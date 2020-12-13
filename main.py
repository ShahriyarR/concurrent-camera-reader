import cv2 as cv
import json
import asyncio
from async_frame_reader.video_async import MultiCameraCapture
from utils.face_detection import run_face_detection
from utils.add_datetime import add_timestamp_to_frame


async def main(captured_obj):
    while True:
        async for camera_name, cap in captured.async_camera_gen():
            frame = await captured_obj.read_frame(cap)
            frame = await add_timestamp_to_frame(frame)
            frame = run_face_detection(frame)

            await captured_obj.show_frame(camera_name, frame)
            if cv.waitKey(1) == 27:
                break


if __name__ == "__main__":
    cameras = json.loads(open('cameras.json').read())
    captured = MultiCameraCapture(sources=cameras)

    asyncio.run(main(captured_obj=captured))
