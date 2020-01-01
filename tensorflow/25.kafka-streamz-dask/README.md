## How-to

1. Run docker compose,

```bash
docker-compose.yaml up --build
```

2. Scale the worker as necessary,

```bash
docker-compose scale worker=2
```

3. Visit passwordless jupyter notebook at [http://localhost:8089](http://localhost:8089/)

4. Run [notebooks/tensorflow-streaming.ipynb](notebooks/tensorflow-streaming.ipynb)

