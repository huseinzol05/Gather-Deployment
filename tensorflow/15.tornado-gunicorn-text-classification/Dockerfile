FROM python:3.6.7-jessie AS base

RUN pip install tensorflow tornado gunicorn numpy

WORKDIR /app

COPY . /app

EXPOSE 8008

CMD gunicorn -b 0.0.0.0:8008 -k tornado -w 2 app:app
