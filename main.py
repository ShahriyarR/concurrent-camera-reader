import cv2 as cv
import datetime
from async_frame_reader.video_async import read_frame

if __name__ == "__main__":
    cap = cv.VideoCapture(0)
    assert cap.isOpened()
    print(cap)
    while True:
        frame = read_frame(cap)

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

        cv.imshow("Frontal Camera", frame)
        if cv.waitKey(1) == 27:
            break
