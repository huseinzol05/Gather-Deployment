FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN pip install water-healer requests streamz==0.5.2

RUN pip install tensorflow transformers

RUN pip install confluent_kafka distributed dask torch

RUN pip install gevent eventlet

COPY ./app /app

WORKDIR /