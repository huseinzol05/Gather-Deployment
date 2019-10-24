FROM ubuntu:18.04 AS base

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    wget

RUN pip3 install numpy "dask[complete]"
RUN pip3 install tensorflow

WORKDIR /app

COPY . /app
