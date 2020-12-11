import cv2 as cv
import datetime
import json
from async_frame_reader.video_async import MultiCameraCapture

if __name__ == "__main__":
    cameras = json.loads(open('cameras.json').read())
    captured = MultiCameraCapture(sources=cameras)

    while True:
        for camera_name, cap in captured.captures.items():
            frame = captured.read_frame(cap)
            font = cv.FONT_HERSHEY_SCRIPT_COMPLEX

            # Get date and time and
            # save it inside a variable
            dt = str(datetime.datetime.now())

            # put the dt variable over the
            # video frame
            frame = cv.putText(frame, dt,
                               (10, 100),
                               font, 1,
                               (210, 155, 155),
                               4, cv.LINE_8)

            cv.imshow(camera_name, frame)
            if cv.waitKey(1) == 27:
                break
