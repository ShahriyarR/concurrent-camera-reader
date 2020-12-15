import cv2 as cv
import json
import asyncio
import uvloop
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from functools import partial
from async_frame_reader.video_async import MultiCameraCapture
from utils.face_detection import run_face_detection
from utils.add_datetime import add_timestamp_to_frame


async def run_fd_time(frame):
    # Show 2nd attempt then
    task1 = asyncio.create_task(add_timestamp_to_frame(frame))
    await task1
    await asyncio.sleep(0.01)


async def run_blocking_func(loop, frame):
    with ProcessPoolExecutor() as pool:
        blocking_func = partial(run_face_detection, frame)
        frame = await loop.run_in_executor(pool, blocking_func)
    return frame

# async def run_fd(loop, executor, frame):
#     task2 = asyncio.create_task(run_face_detection(frame))
#     await task2
#     await asyncio.sleep(0.01)


async def main(captured_obj):
    loop = asyncio.get_running_loop()
    while True:
        async for camera_name, cap in captured.async_camera_gen():
            frame = await captured_obj.read_frame(cap)

            # Show 1st attempt first
            # task1 = asyncio.create_task(add_timestamp_to_frame(frame))
            # task2 = asyncio.create_task(run_face_detection(frame))
            # await asyncio.gather(task1, task2)
            await run_fd_time(frame)
            frame = await run_blocking_func(loop, frame)
            await captured_obj.show_frame(camera_name, frame)
            if cv.waitKey(1) == 27:
                break

            # await  asyncio.sleep(0.01)


if __name__ == "__main__":
    cameras = json.loads(open('cameras.json').read())
    captured = MultiCameraCapture(sources=cameras)
    # executor = ProcessPoolExecutor(max_workers=2)
    uvloop.install()
    asyncio.run(main(captured_obj=captured))
