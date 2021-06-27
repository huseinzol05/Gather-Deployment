FROM ubuntu:16.04 AS base

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-wheel \
    nginx

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

WORKDIR /app

COPY . /app
