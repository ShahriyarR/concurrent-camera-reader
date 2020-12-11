import cv2 as cv
from async_frame_reader.video_async import read_frame

if __name__ == "__main__":
    cap = cv.VideoCapture(0)
    assert cap.isOpened()
    print(cap)
    while True:
        frame = read_frame(cap)
        cv.imshow("Frontal Camera", frame)
        if cv.waitKey(1) == 27:
            break
