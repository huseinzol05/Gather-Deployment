## How-to

1. Make sure you have `Docker` and `Docker-compose`.

2. Build and up the image,
```bash
docker-compose -f docker-compose.yml up --build --remove-orphans
```
```text
flask-inception_1  |  * Debug mode: on
flask-inception_1  |  * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
flask-inception_1  |  * Restarting with stat
```

3. Now you can send any images to classify 1001 classes,
```bash
curl -POST -F file=@husein-tiger.jpg localhost:5000/inception
```
```text
{"label": "soft-coated wheaten terrier"}
```
