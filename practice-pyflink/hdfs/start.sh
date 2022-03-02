/etc/init.d/ssh start

FILE=/app/exist.txt
if [ -f "$FILE" ]; then
    echo 'namenode formatted.'
else
    echo 'formatting namenode.'
    $HADOOP_HOME/bin/hdfs namenode -format
    touch exist.txt
fi

$HADOOP_HOME/sbin/start-yarn.sh
$HADOOP_HOME/sbin/start-dfs.sh
$HADOOP_HOME/bin/hdfs dfs -mkdir /user
$HADOOP_HOME/bin/hdfs dfs -chmod -R 777 /user
$HADOOP_HOME/bin/hdfs dfs -put Iris.csv /user
$HADOOP_HOME/bin/hdfs dfs -mkdir /hive
$HADOOP_HOME/bin/hdfs dfs -chmod -R 777 /hive
tail -f $HADOOP_HOME/logs/hadoop-root-namenode-*.log