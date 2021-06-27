#!/bin/bash

/etc/init.d/ssh start

$HADOOP_HOME/bin/hdfs namenode -format

$HADOOP_HOME/sbin/start-yarn.sh
$HADOOP_HOME/sbin/start-dfs.sh

$HADOOP_HOME/bin/hdfs dfs -mkdir /user
$HADOOP_HOME/bin/hdfs dfs -put $HADOOP_HOME/etc/hadoop/*.xml /user
$HADOOP_HOME/bin/hdfs dfs -put Iris.csv /user
