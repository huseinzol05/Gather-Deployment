FROM ubuntu:16.04 AS base

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-wheel \
    openjdk-8-jdk-headless \
    wget \
    apt-transport-https \
    supervisor

RUN wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | apt-key add -

RUN echo "deb https://artifacts.elastic.co/packages/6.x/apt stable main" | tee -a /etc/apt/sources.list.d/elastic-6.x.list

RUN apt-get update && apt-get install elasticsearch

RUN apt-get update && apt-get install kibana

RUN apt-get update && apt-get install logstash

RUN pip3 install Flask python-json-logger gunicorn python3-logstash

WORKDIR /app

COPY . /app

RUN cp elasticsearch.yml /etc/elasticsearch/

RUN cp kibana.yml /etc/kibana/
