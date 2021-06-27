FROM python:3.6.1 AS base

RUN pip3 install -U textblob ekphrasis
RUN pip3 install flask gunicorn
RUN python3 -m nltk.downloader punkt
RUN python3 -m nltk.downloader wordnet
RUN python3 -m nltk.downloader stopwords
RUN python3 -m textblob.download_corpora

WORKDIR /app

COPY . /app

RUN echo

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

EXPOSE 5000
