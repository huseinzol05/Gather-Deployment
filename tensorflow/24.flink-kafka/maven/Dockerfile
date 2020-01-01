FROM ubuntu:18.04 as base

ARG PYTHON_VERSION=3.6

ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64

RUN apt-get update && apt-get install -y \
    openjdk-8-jdk \
    wget bzip2 \
    python3-pip \
    maven

ENV PYTHON_VERSION $PYTHON_VERSION

RUN apt install git -y

RUN git clone https://github.com/apache/flink.git

WORKDIR /flink

RUN git fetch origin release-1.9

RUN git checkout -b release-1.9 origin/release-1.9

ENV MAVEN_OPTS="-Xmx1024M -Xss128M -XX:MetaspaceSize=512M -XX:MaxMetaspaceSize=1024M -XX:+CMSClassUnloadingEnabled"

RUN mvn clean install -DskipTests -Dfast

WORKDIR /flink/flink-python

RUN python3 setup.py sdist bdist_wheel

RUN pip3 install dist/*.tar.gz

RUN pip3 list|grep flink

ENV FLINK_HOME=/flink/build-target


USER flink
EXPOSE 8081 6123
ENTRYPOINT ["sh", "/docker-entrypoint.sh"]
CMD ["--help"]