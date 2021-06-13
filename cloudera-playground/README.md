## how-to

**Make sure already install Docker and Docker-compose**,

1. Make directory and download necessary jars,

```bash
wget https://repo1.maven.org/maven2/mysql/mysql-connector-java/5.1.49/mysql-connector-java-5.0.8.jar
```

2. Run cloudera quickstart,

```bash
docker run --hostname=quickstart.cloudera \
--privileged=true -t -i -v $(pwd):/cloudera --publish-all=true \
-p8888:8888 -p8088:8088 cloudera/quickstart /usr/bin/docker-quickstart \
--name=cloudera

export JAVA_HOME=/usr/java/jdk1.7.0_67-cloudera
export SQOOP_HOME=/usr/lib/sqoop
export HADOOP_CLASSPATH=$SQOOP_HOME/lib/mysql-connector-java-5.0.8.jar;
cp /cloudera/* $SQOOP_HOME/lib/
```

Login using, `cloudera` / `cloudera`.