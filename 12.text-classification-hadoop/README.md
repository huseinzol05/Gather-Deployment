## How-to

#### [Overview hadoop dashboard](http://localhost:9870)

![alt text]()

You can check HDFS file system, Utilities -> Browse the file system

![alt text]()

#### [Overview hadoop jobs](http://localhost:8088/cluster)

![alt text]()

#### How to remove Yarn job

1. Get job id,
```text
2018-10-28 07:35:18,170 INFO impl.YarnClientImpl: Submitted application application_1540702588430_0006
2018-10-28 07:35:18,261 INFO mapreduce.Job: The url to track the job: http://6de2d313baf4:8088/proxy/application_1540702588430_0006/
2018-10-28 07:35:18,268 INFO mapreduce.Job: Running job: job_1540702588430_0006
```

2. kill the application,
```bash
yarn application -kill application_1540702588430_0006
```

#### HDFS basic command

Delete a HDFS directory,
```bash
hdfs dfs -rm -r /user/output_lower
```

Copy a HDFS directory to your local directory,
```bash
hadoop fs -get /user/output_lower
```

Copy a file to HDFS,
```bash
hadoop fs -put dictionary-test.json /user/dictionary-test.json
```

#### Distributing lowercase

1. Run hadoop streaming,
```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.1.1.jar -file lowercase.py -mapper lowercase.py -file reducer.py -reducer reducer.py -input /user/input_text/* -output /user/output_lower
```

2. Copy the HDFS output to your local,
```bash
hadoop fs -get /user/output_lower
```

#### Distributing text classification

You can the architecture of the model, a very simple model just for an example, [notebook](freeze-model.ipynb)

1. Run hadoop streaming,
```bash
$HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.1.1.jar -file classification.py -file dictionary-test.json -file frozen_model.pb -mapper classification.py -file reducer.py -reducer reducer.py -input /user/input_text/* -output /user/output_classification
```

2. Copy the HDFS output to your local,
```bash
hadoop fs -get /user/output_classification
```
