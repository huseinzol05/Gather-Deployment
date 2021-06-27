FROM ubuntu:16.04 AS base

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-wheel \
    openjdk-8-jdk \
    wget \
    supervisor

RUN pip3 install bs4 requests lxml Flask kafka-python

ADD . /code

WORKDIR /code

RUN wget http://www-us.apache.org/dist/kafka/2.0.0/kafka_2.11-2.0.0.tgz

RUN tar -xvzf kafka_2.11-2.0.0.tgz

RUN cp server.properties kafka_2.11-2.0.0/config/
