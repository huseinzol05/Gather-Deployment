FROM ubuntu:16.04 AS base

RUN apt-get update && apt-get install -y \
    curl \
    git \
    python3 \
    python3-pip \
    python3-wheel \
    wget \
    cmake

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

RUN wget http://download.redis.io/redis-stable.tar.gz && tar xvzf redis-stable.tar.gz

RUN cd redis-stable && make install

WORKDIR /app

COPY . /app
