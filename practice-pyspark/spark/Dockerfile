FROM ubuntu:20.04 AS base

ARG PYTHON_VERSION=3.8

ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64

RUN apt-get update

RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata

RUN apt-get install -y \
    openjdk-8-jdk \
    wget bzip2 \
    python3-pip

ENV HADOOP_HOME /opt/hadoop

ENV HADOOP_VERSION 3.2.2

RUN wget http://www-eu.apache.org/dist/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz && \
    tar -xzf hadoop-${HADOOP_VERSION}.tar.gz && \
    mv hadoop-${HADOOP_VERSION} $HADOOP_HOME && \
    for user in hadoop hdfs yarn mapred; do \
        useradd -U -M -d /opt/hadoop/ --shell /bin/bash ${user}; \
    done && \
    for user in root hdfs yarn mapred; do \
        usermod -G hadoop ${user}; \
    done && \
    echo "export JAVA_HOME=$JAVA_HOME" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh && \
    echo "export HDFS_DATANODE_USER=root" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh && \
    echo "export HDFS_NAMENODE_USER=root" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh && \
    echo "export HDFS_SECONDARYNAMENODE_USER=root" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh && \
    echo "export YARN_RESOURCEMANAGER_USER=root" >> $HADOOP_HOME/etc/hadoop/yarn-env.sh && \
    echo "export YARN_NODEMANAGER_USER=root" >> $HADOOP_HOME/etc/hadoop/yarn-env.sh && \
    echo "PATH=$PATH:$HADOOP_HOME/bin" >> ~/.bashrc

ENV PYTHON_VERSION $PYTHON_VERSION
ENV SCALA_VERSION 2.11.8
ENV SPARK_VERSION 3.1.2
ENV SPARK_BUILD "spark-${SPARK_VERSION}-bin-hadoop2.7"
ENV SPARK_BUILD_URL "https://dist.apache.org/repos/dist/release/spark/spark-${SPARK_VERSION}/${SPARK_BUILD}.tgz"
RUN wget $SPARK_BUILD_URL -O /tmp/spark.tgz && \
    tar -C /opt -xf /tmp/spark.tgz && \
    mv /opt/$SPARK_BUILD /opt/spark && \
    rm /tmp/spark.tgz
ENV SPARK_HOME /opt/spark
ENV PATH $SPARK_HOME/bin:$PATH
ENV PYTHONPATH /opt/spark/python/lib/py4j-0.10.9-src.zip:/opt/spark/python/lib/pyspark.zip:$PYTHONPATH

ENV PYSPARK_PYTHON python3
ENV PYSPARK_DRIVER_PYTHON python3

RUN apt install screen unzip -y

RUN wget https://cdn.mysql.com/archives/mysql-connector-java-5.1/mysql-connector-java-5.1.49.zip -O mysql.zip && \
    unzip mysql.zip && \
    cp mysql-connector-java-5.1.49/mysql-connector-java-5.1.49.jar $SPARK_HOME/jars

RUN wget https://jdbc.postgresql.org/download/postgresql-42.3.0.jar && \
    cp postgresql-42.3.0.jar $SPARK_HOME/jars

RUN wget https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.1.2/spark-sql-kafka-0-10_2.12-3.1.2.jar && \
    cp spark-sql-kafka-0-10_2.12-3.1.2.jar $SPARK_HOME/jars

RUN wget https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_2.12/3.1.2/spark-token-provider-kafka-0-10_2.12-3.1.2.jar && \
    cp spark-token-provider-kafka-0-10_2.12-3.1.2.jar $SPARK_HOME/jars

RUN wget https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/2.6.0/kafka-clients-2.6.0.jar && \
    cp kafka-clients-2.6.0.jar $SPARK_HOME/jars

RUN wget https://repo1.maven.org/maven2/org/apache/commons/commons-pool2/2.6.2/commons-pool2-2.6.2.jar && \
    cp commons-pool2-2.6.2.jar $SPARK_HOME/jars

RUN wget https://raw.githubusercontent.com/yahoo/TensorFlowOnSpark/master/lib/tensorflow-hadoop-1.0-SNAPSHOT.jar && \
    cp tensorflow-hadoop-1.0-SNAPSHOT.jar $SPARK_HOME/jars

ADD hive-site.xml $SPARK_HOME/conf

RUN pip3 install pandas numpy matplotlib seaborn scipy jupyter importlib_metadata spark-nlp==3.3.4

RUN pip3 install delta-spark==1.0.0 --no-deps

RUN pip3 install tensorflowonspark tensorflow==2.5.0 tensorflow-datasets

ENV SHELL /bin/bash

WORKDIR $SPARK_HOME

COPY . $SPARK_HOME