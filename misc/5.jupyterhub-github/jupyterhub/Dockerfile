FROM ubuntu:18.04 AS base

RUN apt-get update && apt-get install -y \
    curl \
    git \
    python3 \
    python3-pip \
    portaudio19-dev \
    libsm6 libxext6 libxrender-dev

RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -
RUN apt-get install -y nodejs

COPY requirements.txt ./
RUN pip3 install -r requirements.txt
RUN pip3 install tornado==5.1.1

RUN npm install -g configurable-http-proxy

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

WORKDIR /app

COPY . /app
