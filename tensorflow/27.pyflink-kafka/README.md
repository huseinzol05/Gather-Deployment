## How-to

1. Run docker compose,

```bash
docker-compose -f docker-compose.yaml up --build
```

2. Scale the worker as necessary,

```bash
docker-compose scale taskmanager=2
```

3. Visit jupyter notebook for easy development at [localhost:8089](http://localhost:8089).

4. Upload python script to cluster using jupyter terminal or docker exec,

```bash
/opt/flink/bin/flink run -py /notebooks/tensorflow_predict.py
```