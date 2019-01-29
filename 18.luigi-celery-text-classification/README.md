## How-to

1. Make sure you installed `Docker` and `Docker-compose`.

2. Spawn the container,
```bash
docker-compose -f docker-compose.yml up --build
```

3. Request to put inside queue,
```bash
curl --form file=@big-text.txt --form topic=big_text localhost:5000/upload
curl --form file=@big-text.txt --form topic=big_text_another localhost:5000/upload
```

## Screenshot

#### Flower dashboard

![alt text](screenshot/flower.png)

#### Luigi dashboard

![alt text](screenshot/luigi.png)
