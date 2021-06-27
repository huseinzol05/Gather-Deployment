# Kafka-cluster

docker compose kafka cluster

## How-to Start

1. Create `backend` network,
```bash
docker network create backend_default
```

2. Build and run docker-compose,
```bash
docker-compose up --build
```

2. Open jupyter notebook on [localhost:8080](http://localhost:8080)

## Test manual partition consumers

Upload [jupyter/test-manual-partition-consumer.ipynb](jupyter/test-manual-partition-consumer.ipynb)

## Test dynamic group consumers

Upload [jupyter/test-dynamic-group-consumer.ipynb](jupyter/test-dynamic-group-consumer.ipynb)
