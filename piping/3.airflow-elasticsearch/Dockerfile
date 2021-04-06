FROM ubuntu:16.04 AS base

RUN apt-get update && apt-get install -y \
    curl \
    python3-pip \
    openjdk-8-jdk-headless \
    apt-transport-https \
    wget

RUN wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | apt-key add -

RUN echo "deb https://artifacts.elastic.co/packages/6.x/apt stable main" | tee -a /etc/apt/sources.list.d/elastic-6.x.list

RUN apt-get update && apt-get install elasticsearch

ENV SLUGIFY_USES_TEXT_UNIDECODE yes

RUN pip3 install Flask apache-airflow elasticsearch

RUN pip3 install tensorflow

RUN pip3 install elasticsearch-dsl

WORKDIR /app

COPY . /app

RUN apt-get install supervisor -y

RUN cp elasticsearch.yml /etc/elasticsearch/

ENV AIRFLOW_HOME /app
