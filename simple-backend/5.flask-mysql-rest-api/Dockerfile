FROM ubuntu:16.04 AS base

ENV MYSQL_PWD husein
RUN echo "mysql-server mysql-server/root_password password $MYSQL_PWD" | debconf-set-selections
RUN echo "mysql-server mysql-server/root_password_again password $MYSQL_PWD" | debconf-set-selections

RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential libssl-dev libffi-dev \
    python3-dev \
    mysql-server \
    python3 \
    python3-pip \
    python3-wheel

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

WORKDIR /app

COPY . /app
