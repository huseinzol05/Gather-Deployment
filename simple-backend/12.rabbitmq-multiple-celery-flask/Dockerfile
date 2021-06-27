FROM ubuntu:16.04 AS base

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    wget \
    rabbitmq-server \
    supervisor

RUN pip3 install Flask celery flower

WORKDIR /app

COPY . /app
