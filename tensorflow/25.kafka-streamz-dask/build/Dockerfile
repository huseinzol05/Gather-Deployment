FROM python:3.7 AS base

WORKDIR /app

RUN pip install tensorflow==1.14 dask[complete] bokeh jupyter streamz confluent-kafka

WORKDIR /notebooks

RUN jupyter notebook --generate-config

RUN echo "" >> /root/.jupyter/jupyter_notebook_config.py
RUN echo "c.NotebookApp.token = ''" >> /root/.jupyter/jupyter_notebook_config.py