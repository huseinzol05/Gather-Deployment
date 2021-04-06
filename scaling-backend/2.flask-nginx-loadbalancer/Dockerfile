FROM ubuntu:16.04 AS base

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-wheel \
    nginx

ADD . /code

WORKDIR /code

RUN pip3 install flask redis gunicorn eventlet
