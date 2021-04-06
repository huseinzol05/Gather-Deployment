FROM ubuntu:16.04 AS base

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip

RUN pip3 install Flask pytest pytest-cov

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

RUN mkdir -p /home/flask
WORKDIR /home/flask

FROM base

COPY . /home/flask
