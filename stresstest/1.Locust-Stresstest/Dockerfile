FROM ubuntu:16.04 AS base

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-wheel \
    supervisor

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

WORKDIR /app

COPY . /app
