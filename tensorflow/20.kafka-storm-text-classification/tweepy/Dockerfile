FROM python:3.6.7-jessie AS base

RUN pip install tweepy unidecode requests
RUN pip install kafka-python

WORKDIR /app

COPY . /app