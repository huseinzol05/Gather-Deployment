FROM python:3.7 AS base

RUN apt-get update && apt-get install -y python3-opencv

RUN pip3 install opencv-python tensorflow==1.15.0 Pillow matplotlib

WORKDIR /app

COPY . /app

ADD http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v2_coco_2018_03_29.tar.gz /app/ssd_mobilenet_v2_coco_2018_03_29.tar.gz

RUN tar -zxf ssd_mobilenet_v2_coco_2018_03_29.tar.gz

RUN pip3 install imagezmq

RUN ls -lh
