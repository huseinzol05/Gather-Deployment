#!/bin/bash

/etc/init.d/ssh start

$HADOOP_HOME/bin/hdfs namenode -format

$HADOOP_HOME/sbin/start-yarn.sh
$HADOOP_HOME/sbin/start-dfs.sh

$HADOOP_HOME/bin/hdfs dfs -mkdir -p /user/hive/warehouse
$HADOOP_HOME/bin/hdfs dfs -chmod 765 /user/hive/warehouse
$HIVE_HOME/bin/schematool -initSchema -dbType derby
$HIVE_HOME/bin/hive --service hiveserver2 --hiveconf hive.server2.thrift.port=10000 --hiveconf hive.root.logger=INFO,console
