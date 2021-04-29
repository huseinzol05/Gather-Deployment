FROM apache/zeppelin:0.9.0 AS base

USER root

ENV FLINK_INSTALL_PATH=/opt
ENV FLINK_HOME $FLINK_INSTALL_PATH/flink
ENV PATH $PATH:$FLINK_HOME/bin

# flink-dist can point to a directory or a tarball on the local system
ENV flink_dist=flink-1.12.2

ADD https://downloads.apache.org/flink/${flink_dist}/${flink_dist}-bin-scala_2.11.tgz flink.tgz

RUN tar -zxf flink.tgz

ADD https://repo.maven.apache.org/maven2/org/apache/flink/flink-shaded-hadoop2-uber/2.8.3-1.8.0/flink-shaded-hadoop2-uber-2.8.3-1.8.0.jar flink-shaded-hadoop2-uber-2.8.3-1.8.0.jar
ENV hadoop_jar=flink-shaded-hadoop2-uber-2.8.3-1.8.0.jar

# Install build dependencies and flink
RUN mkdir -p $FLINK_HOME
RUN cp $hadoop_jar $FLINK_HOME/
RUN cp -r ${flink_dist}/* $FLINK_HOME/

RUN pip3 install --upgrade pip

RUN pip3 install apache-flink

ENV PYFLINK_PYTHON python3

RUN ln -sf /usr/bin/python3 /usr/bin/python && \
    ln -sf /usr/bin/pip3 /usr/bin/pip

USER 1000