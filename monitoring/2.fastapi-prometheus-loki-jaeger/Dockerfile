FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN pip install requests ujson python-json-logger Starlette-Opentracing jaeger-client opentracing-instrumentation

RUN pip install starlette_exporter json-logging

COPY ./app /app

WORKDIR /app/