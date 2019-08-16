# Gather-Tensorflow-Serving
Gather how to deploy tensorflow models as much I can

## Covered

1. Object Detection. Flask SocketIO + WebRTC
2. Object Detection. Flask SocketIO + opencv
3. Speech streaming. Flask SocketIO
4. Text classification. Flask + Gunicorn
5. Image classification. TF Serving
6. Image Classification using Inception. Flask SocketIO
7. Object Detection. Flask + opencv
8. Face-detection using MTCNN. Flask SocketIO + opencv
9. Face-detection using MTCNN. opencv
10. Image classification using Inception. Flask + Docker
11. Image classification using Inception. Flask + EC2 Docker Swarm + Nginx load balancer
12. Text classification. Hadoop streaming MapReduce
13. Text classification. Kafka
14. Text classification. Distributed TF using Flask + Gunicorn + Eventlet
15. Text classification. Tornado + Gunicorn
16. Text classification. Flask + Celery + Hadoop
17. Text classification. Luigi scheduler + Hadoop
18. Text classification. Luigi scheduler + Distributed Celery
19. Text classification. Airflow scheduler + elasticsearch + Flask
20. Text classification. Apache Kafka + Apache Storm

## Technology used

1. [Flask](http://flask.pocoo.org/)
2. [Flask SocketIO](https://flask-socketio.readthedocs.io/)
3. [Gunicorn](https://gunicorn.org/)
4. [Eventlet](http://eventlet.net/)
5. [Tornado](https://www.tornadoweb.org/)
6. [Celery](http://www.celeryproject.org/)
7. [Hadoop](https://hadoop.apache.org/)
8. [Kafka](https://kafka.apache.org/)
9. [Nginx](https://www.nginx.com/)
10. [WebRTC](https://webrtc.org/)
11. [Luigi Spotify](https://luigi.readthedocs.io/en/stable/index.html)
12. [Airflow](https://airflow.apache.org/)
13. [Elastic search](https://www.elastic.co/guide/en/elasticsearch/reference/current/getting-started.html)
14. [Apache Storm](https://storm.apache.org/)

## Printscreen

![alt text](1.object-detection-flasksocketio-webrtc/screenshot.png)

**All folders contain print screens, logs and instructions on how to start.**

## Notes

1. Deploy them on a server, change `local` in code snippets to your own IP.
2. WebRTC chrome only can tested on HTTPS server.
3. When come to real deployment, always prepare for up-scaling architectures. Learn about DevOps.
4. Please aware with your cloud cost!
