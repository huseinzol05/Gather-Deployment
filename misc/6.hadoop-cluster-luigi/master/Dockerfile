FROM ubuntu:16.04 AS base

ENV HADOOP_HOME /opt/hadoop
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    openjdk-8-jdk \
    wget \
    openssh-server

RUN wget http://www-eu.apache.org/dist/hadoop/common/hadoop-3.1.1/hadoop-3.1.1.tar.gz && \
    tar -xzf hadoop-3.1.1.tar.gz && \
    mv hadoop-3.1.1 $HADOOP_HOME

RUN ssh-keygen -t rsa -f ~/.ssh/id_rsa -P '' && \
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys

ADD ../*xml $HADOOP_HOME/etc/hadoop/
ADD ../slaves $HADOOP_HOME/etc/hadoop/

ADD ../ssh_config /root/.ssh/config

RUN pip3 install docutils
RUN pip3 install luigi python-daemon jupyter
RUN echo

RUN jupyter notebook --generate-config

RUN echo "" >> /root/.jupyter/jupyter_notebook_config.py
RUN echo "c.NotebookApp.token = ''" >> /root/.jupyter/jupyter_notebook_config.py

WORKDIR /app

COPY . /app

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
