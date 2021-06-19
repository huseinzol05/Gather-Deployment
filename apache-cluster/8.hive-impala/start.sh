#!/bin/bash

$IMPALA_HOME/bin/start-impala-cluster.py &
$HIVE_HOME/bin/hive --service hiveserver2 --hiveconf hive.server2.thrift.port=10000 --hiveconf hive.root.logger=INFO,console &
wait


