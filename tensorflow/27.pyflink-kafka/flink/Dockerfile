FROM ubuntu:18.04 AS base

ENV PYTHONUNBUFFERED=1

ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64
ENV KM_VERSION=1.2.7
ENV JMX_PORT=9999

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-wheel \
    openjdk-8-jdk \
    wget \
    supervisor

# Flink environment variables
ENV FLINK_INSTALL_PATH=/opt
ENV FLINK_HOME $FLINK_INSTALL_PATH/flink
ENV PATH $PATH:$FLINK_HOME/bin

# flink-dist can point to a directory or a tarball on the local system
ENV flink_dist=flink-1.12.2

RUN wget https://downloads.apache.org/flink/${flink_dist}/${flink_dist}-bin-scala_2.11.tgz

RUN tar -zxf ${flink_dist}-bin-scala_2.11.tgz

RUN wget https://repo.maven.apache.org/maven2/org/apache/flink/flink-shaded-hadoop2-uber/2.8.3-1.8.0/flink-shaded-hadoop2-uber-2.8.3-1.8.0.jar
ENV hadoop_jar=flink-shaded-hadoop2-uber-2.8.3-1.8.0.jar

# Install build dependencies and flink
RUN mkdir $FLINK_HOME
RUN cp $hadoop_jar $FLINK_HOME/
RUN cp -r ${flink_dist}/* $FLINK_HOME/

ENV FLINK_VERSION=1.12.2

ADD https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-connector-kafka_2.11/${FLINK_VERSION}/flink-sql-connector-kafka_2.11-${FLINK_VERSION}.jar $FLINK_HOME/lib/flink-sql-connector-kafka_2.11-${FLINK_VERSION}.jar

RUN pip3 install tensorflow==1.15 apache-flink jupyter

COPY docker-entrypoint.sh /

COPY supervisord.conf /

ENV PYFLINK_PYTHON python3

RUN ln -sf /usr/bin/python3 /usr/bin/python && \
    ln -sf /usr/bin/pip3 /usr/bin/pip

WORKDIR /notebooks

RUN jupyter notebook --generate-config

RUN echo "" >> /root/.jupyter/jupyter_notebook_config.py
RUN echo "c.NotebookApp.token = ''" >> /root/.jupyter/jupyter_notebook_config.py

COPY flink-conf.yaml /opt/flink/conf/

RUN pip3 install supervisor kafka-python==1.4.7

EXPOSE 8081 6123
ENTRYPOINT ["bash", "/docker-entrypoint.sh"]
CMD ["--help"]