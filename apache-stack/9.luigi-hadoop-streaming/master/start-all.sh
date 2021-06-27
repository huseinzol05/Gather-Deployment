service ssh start

$HADOOP_HOME/bin/hdfs namenode -format

$HADOOP_HOME/sbin/start-yarn.sh
$HADOOP_HOME/sbin/start-dfs.sh

luigid --background
jupyter notebook --ip=0.0.0.0 --port=9090 --allow-root
