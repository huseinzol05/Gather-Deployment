FROM huseinzol05/boilerplate-tensorflow-opencv as base

RUN pip3 install Pillow matplotlib

WORKDIR /app

COPY . /app

ADD http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v2_coco_2018_03_29.tar.gz /app/ssd_mobilenet_v2_coco_2018_03_29.tar.gz

RUN tar -zxf ssd_mobilenet_v2_coco_2018_03_29.tar.gz

RUN ls -lh
