import cv2 as cv
import os
import time


def run_face_detection(frame):
    haar_cascades_path = os.path.dirname(cv.__file__) + "/data/haarcascade_frontalface_default.xml"
    eye_cascade_path = os.path.dirname(cv.__file__) + "/data/haarcascade_eye.xml"
    smile_cascade_path = os.path.dirname(cv.__file__) + "/data/haarcascade_smile.xml"

    face_cascade = cv.CascadeClassifier(haar_cascades_path)
    eye_cascade = cv.CascadeClassifier(eye_cascade_path)
    smile_cascade = cv.CascadeClassifier(smile_cascade_path)

    gray = cv.cvtColor(frame[1], cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        print("Face is detected")
        frame = cv.rectangle(frame[1], (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[1][y:y + h, x:x + w]

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

    return frame

