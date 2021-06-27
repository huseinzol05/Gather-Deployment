# Gather-Deployment

Gathers scalable tensorflow and Python infrastructure deployment, Husein Go-To for development, 100% Docker.

## Table of contents
  * [Requirements](#Requirements)
  * [Tensorflow deployment](#tensorflow-deployment)
  * [Simple Backend](#simple-backend)
  * [Apache stack](#apache-stack)
  * [simple data pipeline](#simple-data-pipeline)
  * [Unit test](#unit-test)
  * [Stress test](#stress-test)
  * [Miscellaneous](#Miscellaneous)
  * [Printscreen](#printscreen)

## Requirements

1. Docker
2. Docker compose

## [Tensorflow deployment](tensorflow)

1. Object Detection. _Flask SocketIO + WebRTC_

Stream from webcam using WebRTC -> Flask SocketIO to detect objects -> WebRTC -> Website.

2. Object Detection. _Flask SocketIO + opencv_

Stream from OpenCV -> Flask SocketIO to detect objects -> OpenCV.

3. Speech streaming. _Flask SocketIO_

Stream speech from microphone -> Flask SocketIO to do realtime speech recognition.

4. Text classification. _Flask + Gunicorn_

Serve Tensorflow text model using Flask multiworker + Gunicorn.

5. Image classification. _TF Serving_

Serve image classification model using TF Serving.

6. Image Classification using Inception. _Flask SocketIO_

Stream image using SocketIO -> Flask SocketIO to classify.

7. Object Detection. _Flask + opencv_

Webcam -> Opencv -> Flask -> web dashboard.

8. Face-detection using MTCNN. _Flask SocketIO + opencv_

Stream from OpenCV -> Flask SocketIO to detect faces -> OpenCV.

9. Face-detection using MTCNN. _opencv_

Webcam -> Opencv.

10. Image classification using Inception. _Flask + Docker_

Serve Tensorflow image model using Flask multiworker + Gunicorn on Docker container.

11. Image classification using Inception. _Flask + EC2 Docker Swarm + Nginx load balancer_

Serve inception on multiple AWS EC2, scale using Docker Swarm, balancing using Nginx.

12. Text classification. _Hadoop streaming MapReduce_

Batch processing to classify texts using Tensorflow text model on Hadoop MapReduce.

13. Text classification. _Kafka_

Stream text to Kafka producer and classify using Kafka consumer.

14. Text classification. _Distributed TF using Flask + Gunicorn + Eventlet_

Serve text model on multiple machines using Distributed TF + Flask + Gunicorn + Eventlet. Means that, Distributed TF will split a single neural network model to multiple machines to do feed-forward.

15. Text classification. _Tornado + Gunicorn_

Serve Tensorflow text model using Tornado + Gunicorn.

16. Text classification. _Flask + Celery + Hadoop_

Submit large texts using Flask, signal queue celery job to process using Hadoop, delay Hadoop MapReduce.

17. Text classification. _Luigi scheduler + Hadoop_

Submit large texts on Luigi scheduler, run Hadoop inside Luigi, event based Hadoop MapReduce.

18. Text classification. _Luigi scheduler + Distributed Celery_

Submit large texts on Luigi scheduler, run Hadoop inside Luigi, delay processing.

19. Text classification. _Airflow scheduler + elasticsearch + Flask_

Scheduling based processing using Airflow, store inside elasticsearch, serve it using Flask.

20. Text classification. _Apache Kafka + Apache Storm_

Stream from twitter -> Kafka Producer -> Apache Storm, to do distributed minibatch realtime processing.

21. Text classification. _Dask_

Batch processing to classify texts using Tensorflow text model on Dask.

22. Text classification. _Pyspark_

Batch processing to classify texts using Tensorflow text model on Pyspark.

23. Text classification. _Pyspark streaming + Kafka_

Stream texts to Kafka Producer -> Pyspark Streaming, to do minibatch realtime processing.

24. Text classification. _Streamz + Dask + Kafka_

Stream texts to Kafka Producer -> Streamz -> Dask, to do minibatch realtime processing.

25. Text classification. _FastAPI + Streamz + Water Healer_

Change concurrent requests into mini-batch realtime processing to speed up text classification.

26. Text classification. _PyFlink_

Batch processing to classify texts using Tensorflow text model on Flink batch processing.

27. Text classification. _PyFlink + Kafka_

Stream texts to Kafka Producer -> PyFlink Streaming, to do minibatch realtime processing.

28. Object Detection. _ImageZMQ_

Stream from N camera clients using ImageZMQ -> N slaves ImageZMQ processing -> single dashboard.

## [Simple Backend](simple-backend)

1. Flask
2. Flask with MongoDB
3. REST API Flask
4. Flask Redis PubSub
5. Flask Mysql with REST API
6. Flask Postgres with REST API
7. Flask Elasticsearch
8. Flask Logstash with Gunicorn
9. Flask SocketIO with Redis
10. Multiple Flask with Nginx Loadbalancer
11. Multiple Flask SocketIO with Nginx Loadbalancer
12. RabbitMQ and multiple Celery with Flask
13. Flask + Gunicorn + HAproxy

## [Apache stack](apache-stack)

1. Flask with Hadoop Map Reduce
2. Flask with Kafka
3. Flask with Hadoop Hive
4. PySpark with Jupyter
5. Apache Flink with Jupyter
6. Apache Storm with Redis
7. Apache Flink with Zeppelin and Kafka
8. Kafka cluster + Kafka REST
9. Spotify Luigi + Hadoop streaming

## [simple data pipeline](pipeline)

1. Streaming Tweepy to Elasticsearch
2. Scheduled crawler using Luigi Spotify to Elasticsearch
3. Airflow to Elasticsearch

## [Unit test](unit-test)

1. Pytest

## [Stress test](stresstest)

1. Locust

## [Miscellaneous](misc)

1. Elasticsearch + Kibana + Cerebro
2. Jupyter notebook
3. Jupyterhub
4. Jupyterhub + Github Auth
5. AutoPEP8
6. Graph function dependencies
7. OSRM Malaysia
8. MLFlow

## Printscreen

<img src="tensorflow/1.flasksocketio-webrtc-object-detection/screenshot.png" width="20%">

**All folders contain print screens, logs and instructions on how to start.**
