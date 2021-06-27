## How-to

1. Run `docker-compose`,
```bash
docker-compose up --build
```

2. Scale `sentiment` as many you want,
```bash
docker-compose scale sentiment=2
```

You can see the output from Haproxy,
```text
sentiment-haproxy |   server 5flask-gunicorn-haproxy_sentiment_1 5flask-gunicorn-haproxy_sentiment_1:5000 check inter 2000 rise 2 fall 3
sentiment-haproxy |   server 5flask-gunicorn-haproxy_sentiment_2 5flask-gunicorn-haproxy_sentiment_2:5000 check inter 2000 rise 2 fall 3
```

3. Visit [localhost:5000/classify](http://localhost:5000/classify?text=%20i%20hate%20u%20man),
```text
{"polarity":-0.8,"subjectivity":0.9}
```
