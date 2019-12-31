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

You will get task id,
```text
{"filename": "big-text.txt", "id": "b81ca022-2113-49af-af45-6d3a01052bbf"}
```

You can check the task id from,
```bash
curl localhost:5000/upload_status/task_id
```

Example returned from checking task_id
```text
{"state": "SUCCESS", "result": 42, "status": "upload completed!"}
```

5. Curl to start reducing our uploaded text,
```bash
curl localhost:5000/process
```

You will get task id,
```text
{"id": "161db2ae-5828-4f38-aa6d-e4f630ca92d4"}
```

You can check the task id from,
```bash
curl localhost:5000/classify_text_status/task_id
```

Example returned from checking task_id
```bash
{"state": "PROGRESS", "status": "packageJobJar: [dictionary-test.json, frozen_model.pb, classification.py, reducer.py, /tmp/hadoop-unjar7180917463070947723/] [] /tmp/streamjob7543476212346001034.jar tmpDir=null"}
```

6. Check [LOB9VMEQZE/part-00000](LOB9VMEQZE/part-00000)

Output directory will randomly generated, in my case, I got `LOB9VMEQZE`

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
