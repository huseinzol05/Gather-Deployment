FROM ubuntu:16.04 AS base

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-wheel \
    nginx

ADD . /code

WORKDIR /code

RUN pip3 install mlflow

RUN rm /etc/nginx/sites-enabled/default

RUN cp mlflow-config.conf /etc/nginx/conf.d/

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
