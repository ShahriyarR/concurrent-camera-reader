from typing import Dict
import cv2 as cv
import numpy as np


class MultiCameraCapture:

    def __init__(self, sources: Dict) -> None:
        assert sources
        print(sources)
        self.captures = {}
        for camera_name, link in sources.items():
            cap = cv.VideoCapture(link)
            print(camera_name)
            assert cap.isOpened()
            self.captures[camera_name] = cap

    @staticmethod
    def read_frame(capture):
        # The method for using OpenCV grab() - retrieve()
        # We are not using read() here because, documentation insists that it is slower in multi-thread environment.
        # capture.grab()
        # ret, frame = capture.retrieve()
        ret, frame = capture.read()
        if not ret:
            print("empty frame")
            return
        return frame

    @staticmethod
    def show_frame(window_name: str, frame: np.array):
        cv.imshow(window_name, frame)