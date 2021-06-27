FROM ubuntu:16.04 AS base

RUN apt-get update && apt-get install -y \
    git \
    python3 \
    python3-pip \
    python3-wheel \
    openjdk-8-jdk-headless \
    wget

RUN wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | apt-key add -

RUN echo "deb https://artifacts.elastic.co/packages/6.x/apt stable main" | tee -a /etc/apt/sources.list.d/elastic-6.x.list

RUN apt-get update && apt-get install elasticsearch

RUN apt-get update && apt-get install kibana

WORKDIR /app

COPY . /app

RUN cp elasticsearch.yml /etc/elasticsearch/

RUN cp kibana.yml /etc/kibana/

RUN wget https://github.com/lmenezes/cerebro/releases/download/v0.8.1/cerebro-0.8.1.tgz

RUN tar -zxf cerebro-0.8.1.tgz
