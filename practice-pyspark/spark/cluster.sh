screen -d -m jupyter notebook --NotebookApp.token='' --ip=0.0.0.0 --port=8089 --notebook-dir='/home/data' --allow-root
# $SPARK_HOME/sbin/start-thriftserver.sh
bash -c "/opt/spark/bin/spark-class org.apache.spark.deploy.master.Master"