FROM ubuntu:16.04 AS base

RUN apt-get update && apt-get install -y \
    curl \
    git \
    python3 \
    python3-pip \
    python3-wheel \
    wget \
    openjdk-8-jdk-headless \
    unzip

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

RUN apt-get update && apt-get install -y curl supervisor

WORKDIR /app

RUN wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.3.2.zip

RUN unzip elasticsearch-6.3.2.zip

COPY . /app
