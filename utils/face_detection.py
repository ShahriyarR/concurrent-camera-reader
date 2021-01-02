import cv2 as cv
import os
import time

haar_cascades_path = os.path.dirname(cv.__file__) + "/data/haarcascade_frontalface_default.xml"
eye_cascade_path = os.path.dirname(cv.__file__) + "/data/haarcascade_eye.xml"
smile_cascade_path = os.path.dirname(cv.__file__) + "/data/haarcascade_smile.xml"

face_cascade = cv.CascadeClassifier(haar_cascades_path)
eye_cascade = cv.CascadeClassifier(eye_cascade_path)
smile_cascade = cv.CascadeClassifier(smile_cascade_path)


def run_face_detection(frame):
    camera_name = frame[0]
    frame_status = frame[-1]
    current_frame = frame[1]

    if not frame_status:
        gray = cv.cvtColor(current_frame, cv.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            print("Face is detected")
            frame = cv.rectangle(current_frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = current_frame[y:y + h, x:x + w]

            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex, ey, ew, eh) in eyes:
                print("Eye is detected")
                cv.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

            smiles = smile_cascade.detectMultiScale(roi_gray, 1.8, 20)
            for (sx, sy, sw, sh) in smiles:
                print("Smile is detected")
                cv.rectangle(roi_color, (sx, sy), ((sx + sw), (sy + sh)), (0, 0, 255), 2)

        # Simulation of some blocking code
        time.sleep(0.5)
        frame_status = True
        print("end of face detection", [camera_name, current_frame, frame_status])
        return [camera_name, current_frame, frame_status]
    return frame

