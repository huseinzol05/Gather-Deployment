FROM apache/nifi:latest AS base

USER root

ADD mysql-connector-java-5.1.49.jar /opt/nifi/drivers/mysql-connector-java-5.1.49.jar

WORKDIR /opt/nifi/drivers

RUN wget https://repo.maven.apache.org/maven2/org/apache/hive/hive-jdbc/3.1.0/hive-jdbc-3.1.0-standalone.jar