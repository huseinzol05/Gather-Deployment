FROM ubuntu:20.04 AS base

ARG PYTHON_VERSION=3.8

ENV PYTHONUNBUFFERED=1

ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64
ENV KM_VERSION=1.2.7
ENV JMX_PORT=9999

RUN apt-get update

RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata

RUN apt-get install -y \
    python3 \
    python3-pip \
    python3-wheel \
    openjdk-8-jdk \
    wget \
    screen \
    unzip

# Flink environment variables
ENV FLINK_INSTALL_PATH=/opt
ENV FLINK_HOME $FLINK_INSTALL_PATH/flink
ENV PATH $PATH:$FLINK_HOME/bin

RUN mkdir $FLINK_HOME

# flink-dist can point to a directory or a tarball on the local system
ENV FLINK_VERSION=1.13.6
ENV flink_dist=flink-$FLINK_VERSION

RUN wget https://downloads.apache.org/flink/${flink_dist}/${flink_dist}-bin-scala_2.11.tgz -O flink.tgz && \
    tar -zxf flink.tgz && \
    cp -r ${flink_dist}/* $FLINK_HOME/

RUN wget -P $FLINK_HOME/lib/ https://repo.maven.apache.org/maven2/org/apache/flink/flink-shaded-hadoop2-uber/2.8.3-1.8.0/flink-shaded-hadoop2-uber-2.8.3-1.8.0.jar

RUN wget -P $FLINK_HOME/lib/ https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-avro-confluent-registry/${FLINK_VERSION}/flink-sql-avro-confluent-registry-${FLINK_VERSION}.jar
RUN wget -P $FLINK_HOME/lib/ https://repo.maven.apache.org/maven2/org/apache/flink/flink-parquet_2.11/${FLINK_VERSION}/flink-parquet_2.11-${FLINK_VERSION}.jar

RUN wget -P $FLINK_HOME/lib/ https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-connector-kafka_2.11/${FLINK_VERSION}/flink-sql-connector-kafka_2.11-${FLINK_VERSION}.jar
RUN wget -P $FLINK_HOME/lib/ https://repo.maven.apache.org/maven2/org/apache/flink/flink-connector-jdbc_2.11/${FLINK_VERSION}/flink-connector-jdbc_2.11-${FLINK_VERSION}.jar
RUN wget -P $FLINK_HOME/lib/ https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-connector-hive-3.1.2_2.11/${FLINK_VERSION}/flink-sql-connector-hive-3.1.2_2.11-${FLINK_VERSION}.jar
RUN wget -P $FLINK_HOME/lib/ https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-connector-hbase-2.2_2.11/${FLINK_VERSION}/flink-sql-connector-hbase-2.2_2.11-${FLINK_VERSION}.jar
RUN wget -P $FLINK_HOME/lib/ https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-connector-elasticsearch6_2.11/${FLINK_VERSION}/flink-sql-connector-elasticsearch6_2.11-${FLINK_VERSION}.jar

RUN wget -P $FLINK_HOME/lib/ https://repo1.maven.org/maven2/org/apache/hive/hive-exec/3.1.2/hive-exec-3.1.2.jar
RUN wget -P $FLINK_HOME/lib/ https://repo1.maven.org/maven2/org/apache/thrift/libfb303/0.9.3/libfb303-0.9.3.jar
RUN wget -P $FLINK_HOME/lib/ https://repo.maven.apache.org/maven2/mysql/mysql-connector-java/8.0.19/mysql-connector-java-8.0.19.jar
RUN wget -P $FLINK_HOME/lib https://jdbc.postgresql.org/download/postgresql-42.2.19.jar

RUN wget -P $FLINK_HOME/lib https://repo.maven.apache.org/maven2/org/apache/hudi/hudi-flink-bundle_2.11/0.10.1/hudi-flink-bundle_2.11-0.10.1.jar

ENV PATH $FLINK_HOME/bin:$PATH

COPY docker-entrypoint.sh /

ENV PYFLINK_PYTHON python3

RUN ln -sf /usr/bin/python3 /usr/bin/python && \
    ln -sf /usr/bin/pip3 /usr/bin/pip

WORKDIR $FLINK_HOME

COPY flink-conf.yaml $FLINK_HOME/conf/

ENV HADOOP_HOME /opt/hadoop
ENV HADOOP_VERSION 3.2.3

RUN wget http://www-eu.apache.org/dist/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz && \
    tar -xzf hadoop-${HADOOP_VERSION}.tar.gz && \
    mv hadoop-${HADOOP_VERSION} $HADOOP_HOME

ENV PATH $HADOOP_HOME/bin:$PATH

ADD hive-site.xml /opt/hive-conf/

RUN pip3 install jupyter apache-flink==1.13.6

RUN pip3 install pydoop

RUN pip3 install sklearn tqdm

EXPOSE 8081 6123
ENTRYPOINT ["bash", "/docker-entrypoint.sh"]
CMD ["--help"]