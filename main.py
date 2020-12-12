import cv2 as cv
import datetime
import json
from async_frame_reader.video_async import MultiCameraCapture
from utils.face_detection import run_face_detection
from utils.add_datetime import add_timestamp_to_frame

if __name__ == "__main__":
    cameras = json.loads(open('cameras.json').read())
    captured = MultiCameraCapture(sources=cameras)

    while True:
        for camera_name, cap in captured.captures.items():
            frame = captured.read_frame(cap)
            frame = add_timestamp_to_frame(frame)
            frame = run_face_detection(frame)

            cv.imshow(camera_name, frame)
            if cv.waitKey(1) == 27:
                break
