FROM ubuntu:16.04 AS base

ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64
ENV KM_VERSION=1.2.7
ENV JMX_PORT=9999

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-wheel \
    openjdk-8-jdk \
    wget \
    supervisor

ADD . /code

WORKDIR /code

RUN tar -xvzf kafka_2.11-2.0.0.tgz

RUN cp server.properties kafka_2.11-2.0.0/config/
RUN cp server2.properties kafka_2.11-2.0.0/config/
RUN cp server3.properties kafka_2.11-2.0.0/config/

RUN echo
