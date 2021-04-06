FROM debian:stretch-slim AS base

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip

RUN pip3 install scipy matplotlib seaborn numpy sklearn scikit-learn tensorflow jupyter

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

RUN jupyter notebook --generate-config

RUN echo "" >> /root/.jupyter/jupyter_notebook_config.py
RUN echo "c.NotebookApp.token = ''" >> /root/.jupyter/jupyter_notebook_config.py

WORKDIR /app
