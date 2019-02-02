# Gather-Tensorflow-Serving
Gather how to deploy tensorflow models as much I can

## Covered

1. Object Detection using Flask SocketIO for WebRTC
2. Object Detection using Flask SocketIO for opencv
3. Speech streaming using Flask SocketIO
4. Classification using Flask + Gunicorn
5. Classification using TF Serving
6. Inception Classification using Flask SocketIO
7. Object Detection using Flask + opencv
8. Face-detection using Flask SocketIO for opencv
9. Face-detection for opencv
10. Inception with Flask using Docker
11. Multiple Inception with Flask using EC2 Docker Swarm + Nginx load balancer
12. Text classification using Hadoop streaming MapReduce
13. Text classification using Kafka
14. Text classification on Distributed TF using Flask + Gunicorn + Eventlet
15. Text classification using Tornado + Gunicorn
16. Celery with Hadoop for Massive text classification using Flask
17. Luigi scheduler with Hadoop for Massive text classification
18. Luigi scheduler with Distributed Celery for Massive text classification
19. Airflow scheduler with elasticsearch for Massive text classification using Flask

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

## Printscreen

![alt text](1.object-detection-flasksocketio-webrtc/screenshot.png)

**All folders contain print screens, logs and instructions on how to start.**

## Notes

1. Deploy them on a server, change `local` in code snippets to your own IP.
2. WebRTC chrome only can tested on HTTPS server.
3. When come to real deployment, always prepare for up-scaling architectures. Learn about DevOps.
4. Please aware with your cloud cost!
