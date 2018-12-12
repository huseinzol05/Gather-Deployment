## How-to

1. Make sure you installed `Docker` and `Docker-compose`.

2. Spawn the container,
```bash
compose/build
```

3. Open new tab / window for terminal and access bash inside that container,
```bash
compose/bash
python3 app.py
```

4. Curl upload file,
```bash
curl --form file=@big-text.txt --form split_size=10 localhost:5000/upload
```

You will task id,
```text
{"filename": "big-text.txt", "id": "b81ca022-2113-49af-af45-6d3a01052bbf"}
```

You can check the task id from,
```bash
curl localhost:5000/upload_status/task_id
```

Output from celery,
```text
tf-hadoop_1  | [2018-12-12 01:54:17,549: DEBUG/MainProcess] Task accepted: app.upload_files_dfs[bc5c1fee-6f0d-4a63-b06e-ddfbe5670b36] pid:1609
tf-hadoop_1  | [2018-12-12 01:54:17,551: WARNING/ForkPoolWorker-4] 0: uploading /user/input_text/0-big-text.txt
tf-hadoop_1  | [2018-12-12 01:54:17,551: WARNING/ForkPoolWorker-4] 0: /opt/hadoop/bin/hdfs dfs -put 0-big-text.txt /user/input_text/0-big-text.txt
tf-hadoop_1  | [2018-12-12 01:54:17,556: WARNING/ForkPoolWorker-4] 1: uploading /user/input_text/1-big-text.txt
tf-hadoop_1  | [2018-12-12 01:54:17,556: WARNING/ForkPoolWorker-4] 1: /opt/hadoop/bin/hdfs dfs -put 1-big-text.txt /user/input_text/1-big-text.txt
tf-hadoop_1  | [2018-12-12 01:54:17,558: WARNING/ForkPoolWorker-4] 2: uploading /user/input_text/2-big-text.txt
tf-hadoop_1  | [2018-12-12 01:54:17,558: WARNING/ForkPoolWorker-4] 2: /opt/hadoop/bin/hdfs dfs -put 2-big-text.txt /user/input_text/2-big-text.txt
tf-hadoop_1  | [2018-12-12 01:54:17,569: WARNING/ForkPoolWorker-4] 3: uploading /user/input_text/3-big-text.txt
tf-hadoop_1  | [2018-12-12 01:54:17,569: WARNING/ForkPoolWorker-4] 3: /opt/hadoop/bin/hdfs dfs -put 3-big-text.txt /user/input_text/3-big-text.txt
tf-hadoop_1  | [2018-12-12 01:54:17,571: WARNING/ForkPoolWorker-4] 4: uploading /user/input_text/4-big-text.txt
tf-hadoop_1  | [2018-12-12 01:54:17,572: WARNING/ForkPoolWorker-4] 4: /opt/hadoop/bin/hdfs dfs -put 4-big-text.txt /user/input_text/4-big-text.txt
tf-hadoop_1  | [2018-12-12 01:54:17,583: WARNING/ForkPoolWorker-4] 5: uploading /user/input_text/5-big-text.txt
tf-hadoop_1  | [2018-12-12 01:54:17,583: WARNING/ForkPoolWorker-4] 5: /opt/hadoop/bin/hdfs dfs -put 5-big-text.txt /user/input_text/5-big-text.txt
tf-hadoop_1  | [2018-12-12 01:54:17,587: WARNING/ForkPoolWorker-4] 6: uploading /user/input_text/6-big-text.txt
tf-hadoop_1  | [2018-12-12 01:54:17,587: WARNING/ForkPoolWorker-4] 6: /opt/hadoop/bin/hdfs dfs -put 6-big-text.txt /user/input_text/6-big-text.txt
tf-hadoop_1  | [2018-12-12 01:54:17,590: WARNING/ForkPoolWorker-4] 7: uploading /user/input_text/7-big-text.txt
tf-hadoop_1  | [2018-12-12 01:54:17,590: WARNING/ForkPoolWorker-4] 7: /opt/hadoop/bin/hdfs dfs -put 7-big-text.txt /user/input_text/7-big-text.txt
tf-hadoop_1  | [2018-12-12 01:54:17,593: WARNING/ForkPoolWorker-4] 8: uploading /user/input_text/8-big-text.txt
tf-hadoop_1  | [2018-12-12 01:54:17,593: WARNING/ForkPoolWorker-4] 8: /opt/hadoop/bin/hdfs dfs -put 8-big-text.txt /user/input_text/8-big-text.txt
tf-hadoop_1  | [2018-12-12 01:54:17,596: WARNING/ForkPoolWorker-4] 9: uploading /user/input_text/9-big-text.txt
tf-hadoop_1  | [2018-12-12 01:54:17,596: WARNING/ForkPoolWorker-4] 9: /opt/hadoop/bin/hdfs dfs -put 9-big-text.txt /user/input_text/9-big-text.txt
tf-hadoop_1  | [2018-12-12 01:54:17,614: INFO/ForkPoolWorker-4] Task app.upload_files_dfs[bc5c1fee-6f0d-4a63-b06e-ddfbe5670b36] succeeded in 0.06530934385955334s: {'result': 42, 'status': 'upload completed!'}
```

5. Curl to start reducing our uploaded text,
```bash
curl localhost:5000/process
```

You will task id,
```text
{"id": "161db2ae-5828-4f38-aa6d-e4f630ca92d4"}
```

You can check the task id from,
```bash
curl localhost:5000/classify_text_status/task_id
```

Output from celery,
```text
tf-hadoop_1  | 2018-12-12 01:54:25,611 INFO mapred.FileInputFormat: Total input files to process : 11
tf-hadoop_1  | 2018-12-12 01:54:26,483 INFO mapreduce.JobSubmitter: number of splits:11
tf-hadoop_1  | 2018-12-12 01:54:26,502 INFO Configuration.deprecation: yarn.resourcemanager.system-metrics-publisher.enabled is deprecated. Instead, use yarn.system-metrics-publisher.enabled
tf-hadoop_1  | 2018-12-12 01:54:26,555 INFO mapreduce.JobSubmitter: Submitting tokens for job: job_1544579631508_0001
tf-hadoop_1  | 2018-12-12 01:54:26,556 INFO mapreduce.JobSubmitter: Executing with tokens: []
tf-hadoop_1  | 2018-12-12 01:54:26,675 INFO conf.Configuration: resource-types.xml not found
tf-hadoop_1  | 2018-12-12 01:54:26,676 INFO resource.ResourceUtils: Unable to find 'resource-types.xml'.
tf-hadoop_1  | 2018-12-12 01:54:26,837 INFO impl.YarnClientImpl: Submitted application application_1544579631508_0001
tf-hadoop_1  | 2018-12-12 01:54:26,864 INFO mapreduce.Job: The url to track the job: http://853f8b26e89e:8088/proxy/application_1544579631508_0001/
tf-hadoop_1  | 2018-12-12 01:54:26,865 INFO mapreduce.Job: Running job: job_1544579631508_0001
tf-hadoop_1  | 2018-12-12 01:54:31,925 INFO mapreduce.Job: Job job_1544579631508_0001 running in uber mode : false
tf-hadoop_1  | 2018-12-12 01:54:31,926 INFO mapreduce.Job:  map 0% reduce 0%
tf-hadoop_1  | 2018-12-12 01:54:42,000 INFO mapreduce.Job:  map 55% reduce 0%
tf-hadoop_1  | 2018-12-12 01:54:50,036 INFO mapreduce.Job:  map 100% reduce 0%
tf-hadoop_1  | 2018-12-12 01:54:52,043 INFO mapreduce.Job:  map 100% reduce 100%
tf-hadoop_1  | 2018-12-12 01:54:53,051 INFO mapreduce.Job: Job job_1544579631508_0001 completed successfully
```

6. Check [output_classification/part-00000](output_classification/part-00000)
```text
6 of americans clicked the wrong button: negative
780 in food stamps plus wic thats some lavish dining: positive
a chuckleworthy irony: negative
a press release right before a long holiday surely this isnt an attempt to bury such big change in policy: positive
a prosperity gospel preacher in a megachurch turns out to be corrupt what next is someone going to tell me that jorge bergoglio is a papist: positive
a smart guy like bill nye should know the moon is made of glowy stuff: positive
abort all the things: negative
```

## Extra

#### Basic hadoop

[Overview hadoop dashboard](http://localhost:9870)

![alt text](printscreen/2.png)

You can check HDFS file system, Utilities -> Browse the file system

![alt text](printscreen/3.png)

[Overview hadoop jobs](http://localhost:8088/cluster)

![alt text](printscreen/1.png)

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
