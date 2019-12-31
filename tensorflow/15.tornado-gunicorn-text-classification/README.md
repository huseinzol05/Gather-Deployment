## How-to

1. Build and run the Dockerfile,
```bash
docker build -t tornado-tf . && docker run -p 8008:8008 tornado-tf
```
```text
[2018-11-18 12:29:31 +0000] [6] [INFO] Starting gunicorn 19.9.0
[2018-11-18 12:29:31 +0000] [6] [INFO] Listening at: http://0.0.0.0:8008 (6)
[2018-11-18 12:29:31 +0000] [6] [INFO] Using worker: tornado
[2018-11-18 12:29:31 +0000] [9] [INFO] Booting worker with pid: 9
[2018-11-18 12:29:31 +0000] [11] [INFO] Booting worker with pid: 11
```

2. Curl some request,
```bash
curl http://localhost:8008/classifier?sentence=this%20is%20shit
```
```text
{"sentiment": "negative"}
```
