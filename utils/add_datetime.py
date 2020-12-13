import datetime
import cv2 as cv
import asyncio


async def add_timestamp_to_frame(frame):
    font = cv.FONT_HERSHEY_SCRIPT_COMPLEX

    # Get date and time and
    # save it inside a variable
    dt = str(datetime.datetime.now())

    # put the dt variable over the
    # video frame
    cv.putText(frame, dt,
                       (10, 100),
                       font, 1,
                       (210, 155, 155),
                       4, cv.LINE_8)

    await asyncio.sleep(0.01)
