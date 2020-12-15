FROM python:3.8

WORKDIR /app

RUN python -m pip install --upgrade pip
RUN pip install opencv-python==4.1.2.30
RUN pip install uvloop
RUN apt-get update
RUN apt-get install -y libgl1-mesa-glx
RUN apt-get install -y xauth

COPY . .
