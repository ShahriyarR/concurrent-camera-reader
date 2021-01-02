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


async def run_fd_time(queue_, frame):
    # Show 2nd attempt then
    task1 = asyncio.create_task(add_timestamp_to_frame(frame))
    await queue_.put(await task1)
    # await asyncio.sleep(0.01)


async def run_blocking_func(loop_, queue_):
    with ProcessPoolExecutor() as pool:
        frame = await queue_.get()
        blocking_func = partial(run_face_detection, frame)
        frame = await loop_.run_in_executor(pool, blocking_func)
        frame[-1] = True
        await queue_.put(frame)
        # await asyncio.sleep(0.01)


async def produce(queue_, captured_obj):
    while True:
        async for camera_name, cap in captured_obj.async_camera_gen():
            # Read the frame and put it into the Queue
            frame = await asyncio.create_task(captured_obj.read_frame(cap), name="frame_reader")
            print("inside producer")
            await queue_.put([camera_name, frame, None])
            # await asyncio.sleep(0.01)

        # To indicate that producer is done
        await asyncio.sleep(0.01)


async def consume(loop_, queue_, captured_obj):
    while True:
        # If there is something in Queue
        if queue_.qsize():
            # Read it from queue
            frame = await queue_.get()
            print("inside consumer")
            # Add timestamp and put back the frame
            await run_fd_time(queue_, frame)
            # Show the frame
            task1 = asyncio.create_task(captured_obj.show_frame(queue_), name="show_frame")
            await task1
            # # Apply Face detection
            # task2 = asyncio.create_task(run_blocking_func(loop_, queue_))

            # await asyncio.wait([task1, task2], return_when=asyncio.FIRST_COMPLETED)
            if cv.waitKey(1) == 27:
                break
            # await asyncio.sleep(0.01)
        else:
            # To indicate that queue is empty
            await asyncio.sleep(0.01)


async def run(loop_, queue_, captured_obj):
    producer_task = asyncio.create_task(produce(queue_, captured_obj), name="producer-task")
    consumer_task = asyncio.create_task(consume(loop_, queue_, captured_obj), name="consumer-task")
    await asyncio.gather(producer_task, consumer_task)


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
    queue = asyncio.LifoQueue(maxsize=4)

    # Signal handler
    signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)
    for s in signals:
        loop.add_signal_handler(
            s, lambda f=s: asyncio.create_task(shutdown_(s, loop)))

    try:
        loop.run_until_complete(run(loop_=loop, queue_=queue, captured_obj=captured))
    # except KeyboardInterrupt:
    #     loop.run_until_complete(asyncio.ensure_future(shutdown_(loop)))
    finally:
        print("Successfully shutdown service")
        loop.close()
