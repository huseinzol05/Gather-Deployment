FROM openjdk:8 AS base

ENV HADOOP_HOME /opt/hadoop
ENV HIVE_HOME /opt/hive
ENV IMPALA_HOME /opt/impala
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64

RUN apt-get update && apt-get install -y ssh wget

RUN wget http://www-eu.apache.org/dist/hadoop/common/hadoop-3.1.1/hadoop-3.1.1.tar.gz && \
    tar -xzf hadoop-3.1.1.tar.gz && \
    mv hadoop-3.1.1 $HADOOP_HOME && \
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

RUN apt-get install openssh-client -y && \
    ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa && \
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys && \
    chmod 0600 ~/.ssh/authorized_keys

ADD *xml $HADOOP_HOME/etc/hadoop/

ADD ssh_config /root/.ssh/config

RUN wget https://archive.apache.org/dist/hive/hive-3.1.0/apache-hive-3.1.0-bin.tar.gz
RUN tar -xzf apache-hive-3.1.0-bin.tar.gz && mv apache-hive-3.1.0-bin $HIVE_HOME

RUN wget http://archive.apache.org/dist/impala/3.3.0/apache-impala-3.3.0.tar.gz
RUN tar -xzf apache-impala-3.3.0.tar.gz && mv apache-impala-3.3.0 $IMPALA_HOME

RUN /etc/init.d/ssh start

RUN $HADOOP_HOME/bin/hdfs namenode -format

RUN $HADOOP_HOME/sbin/start-yarn.sh
RUN $HADOOP_HOME/sbin/start-dfs.sh

RUN $HADOOP_HOME/bin/hdfs dfs -mkdir -p /user/hive/warehouse
RUN $HADOOP_HOME/bin/hdfs dfs -chmod 765 /user/hive/warehouse
RUN $HIVE_HOME/bin/schematool -initSchema -dbType derby

RUN $IMPALA_HOME/bin/impala-config.sh