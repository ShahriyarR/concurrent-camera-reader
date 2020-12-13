from typing import Dict
import cv2 as cv
import numpy as np
import asyncio


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
    async def read_frame(capture):
        # The method for using OpenCV grab() - retrieve()
        # We are not using read() here because, documentation insists that it is slower in multi-thread environment.
        capture.grab()
        ret, frame = capture.retrieve()
        if not ret:
            print("empty frame")
            return
        return frame

    @staticmethod
    async def show_frame(window_name: str, frame: np.array):
        # Just making the OpenCV imshow awaitable in order to be able to run through asyncio
        cv.imshow(window_name, frame)
        await asyncio.sleep(0.01)

    async def async_camera_gen(self):
        for camera_name, capture in self.captures.items():
            yield camera_name, capture
            await asyncio.sleep(0.001)

