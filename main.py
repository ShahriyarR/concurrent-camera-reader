import cv2 as cv
import json
import asyncio
import uvloop
import signal
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


async def run_blocking_func(loop_, frame):
    # TODO: Show ThreadPoolExecutor
    with ProcessPoolExecutor() as pool:
        blocking_func = partial(run_face_detection, frame)
        frame = await loop.run_in_executor(pool, blocking_func)
        await asyncio.sleep(0.01)
    return frame


async def main(loop_, captured_obj):
    while True:
        async for camera_name, cap in captured.async_camera_gen():
            frame = await asyncio.create_task(captured_obj.read_frame(cap), name="frame_reader")
            await asyncio.create_task(run_fd_time(frame), name="add_timestamp")

            task1 = asyncio.create_task(captured_obj.show_frame(camera_name, frame), name="show_frame")
            task2 = asyncio.create_task(run_blocking_func(loop_, frame))
            await asyncio.wait([task1, task2], return_when=asyncio.FIRST_COMPLETED)
            if cv.waitKey(1) == 27:
                break


async def shutdown_(signal_, loop_):
    """
    For normal shutdown process.
    """
    print(f"Received signal -> {signal_}")
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    [task.cancel() for task in tasks]
    print(f"Cancelling {len(tasks)} tasks")
    await asyncio.gather(*tasks)

    loop_.stop()


if __name__ == "__main__":
    cameras = json.loads(open('cameras.json').read())
    captured = MultiCameraCapture(sources=cameras)

    uvloop.install()
    loop = asyncio.get_event_loop()

    # Signal handler
    signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)
    for s in signals:
        loop.add_signal_handler(
            s, lambda f=s: asyncio.create_task(shutdown_(s, loop)))

    try:
        loop.run_until_complete(main(loop_=loop, captured_obj=captured))
    # except KeyboardInterrupt:
    #     loop.run_until_complete(asyncio.ensure_future(shutdown_(loop)))
    finally:
        print("Successfully shutdown service")
        loop.close()
