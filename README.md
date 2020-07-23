# Gather-Deployment

Gathers scalable tensorflow and infrastructure deployment, reusable purpose in the future.

## Table of contents
  * [Tensorflow deployment](#tensorflow-deployment)

## Tensorflow deployment

1. Object Detection. _Flask SocketIO + WebRTC_

-   Stream from webcam using WebRTC -> Flask SocketIO to detect objects -> WebRTC -> Website.

2. Object Detection. _Flask SocketIO + opencv_

-   Stream from OpenCV -> Flask SocketIO to detect objects -> OpenCV.

3. Speech streaming. _Flask SocketIO_

-   Stream speech from microphone -> Flask SocketIO to do realtime speech recognition.

4. Text classification. _Flask + Gunicorn_

-   Serve Tensorflow text model using Flask multiworker + Gunicorn.

5. Image classification. _TF Serving_

-   Serve image classification model using TF Serving.

6. Image Classification using Inception. _Flask SocketIO_

-   Stream image using SocketIO -> Flask SocketIO to classify.

7. Object Detection. _Flask + opencv_

-   Webcam -> Opencv -> Flask -> web dashboard.

8. Face-detection using MTCNN. _Flask SocketIO + opencv_

-   Stream from OpenCV -> Flask SocketIO to detect faces -> OpenCV.

9. Face-detection using MTCNN. _opencv_

-   Webcam -> Opencv.

10. Image classification using Inception. _Flask + Docker_

-   Serve Tensorflow image model using Flask multiworker + Gunicorn on Docker container.

11. Image classification using Inception. _Flask + EC2 Docker Swarm + Nginx load balancer_

-   Serve inception on multiple AWS EC2, scale using Docker Swarm, balancing using Nginx.

12. Text classification. _Hadoop streaming MapReduce_

-   Batch processing to classify texts using Tensorflow text model on Hadoop MapReduce.

13. Text classification. _Kafka_

-   Stream text to Kafka producer and classify using Kafka consumer.

14. Text classification. _Distributed TF using Flask + Gunicorn + Eventlet_

-   Serve text model on multiple machines using Distributed TF + Flask + Gunicorn + Eventlet. Means that, Distributed TF will split a single neural network model to multiple machines to do feed-forward.

15. Text classification. _Tornado + Gunicorn_

-   Serve Tensorflow text model using Tornado + Gunicorn.

16. Text classification. _Flask + Celery + Hadoop_

-   Submit large texts using Flask, signal queue celery job to process using Hadoop, delay Hadoop MapReduce.

17. Text classification. _Luigi scheduler + Hadoop_

-   Submit large texts on Luigi scheduler, run Hadoop inside Luigi, event based Hadoop MapReduce.

18. Text classification. _Luigi scheduler + Distributed Celery_

-   Submit large texts on Luigi scheduler, run Hadoop inside Luigi, delay processing.

19. Text classification. _Airflow scheduler + elasticsearch + Flask_

-   Scheduling based processing using Airflow, store inside elasticsearch, serve it using Flask.

20. Text classification. _Apache Kafka + Apache Storm_

-   Stream from twitter -> Kafka Producer -> Apache Storm, to do distributed minibatch realtime processing.

21. Text classification. _Dask_

-   Batch processing to classify texts using Tensorflow text model on Dask.

22. Text classification. _Pyspark_

-   Batch processing to classify texts using Tensorflow text model on Pyspark.

23. Text classification. _Pyspark streaming + Kafka_

-   Stream texts to Kafka Producer -> Pyspark Streaming, to do minibatch realtime processing.

24. Text classification. _PyFlink_

-   Batch processing to classify texts using Tensorflow text model on Flink batch processing.

25. Text classification. _Streamz + Dask + Kafka_

-   Stream texts to Kafka Producer -> Streamz -> Dask, to do minibatch realtime processing.

26. Text classification. _FastAPI + Streamz + Water Healer_

-   Change concurrent requests into mini-batch realtime processing to speed up text classification.

### Printscreen

<img src="tensorflow/1.flasksocketio-webrtc-object-detection/screenshot.png" width="50%">

**All folders contain print screens, logs and instructions on how to start.**

### Notes

1. Deploy them on a server, change `local` in code snippets to your own IP.
2. WebRTC chrome only can tested on HTTPS server.
3. When come to real deployment, always prepare for up-scaling architectures. Learn about DevOps.
4. Please aware with your cloud cost!
