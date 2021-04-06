service ssh start

$HADOOP_HOME/bin/hdfs namenode -format

$HADOOP_HOME/sbin/start-yarn.sh
$HADOOP_HOME/sbin/start-dfs.sh

tail -f hadoop-root-resourcemanager-*.log | while read line; do echo $line; sleep 1; done
