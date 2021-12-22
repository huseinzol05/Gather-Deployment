# Practice-Pyspark

Gathers data science and machine learning problem solving using PySpark and Hadoop.

<img src="https://cdn-images-1.medium.com/max/1600/0*8D301fHKliN6r5Km.png" align="right" width="20%">

## How-to

1. Run HDFS and PostgreSQL for Hive Metastore,

```bash
docker container rm -f hdfs postgres
docker-compose -f misc.yaml up --build
```

2. Create Hive metastore in PostgreSQL,

```bash
PGPASSWORD=postgres docker exec -it postgres psql -U postgres -d postgres -c "$(cat hive-schema-3.1.0.postgres.sql)"
```

3. Build image,

```bash
docker build -t spark spark
```

4. Run docker compose,

```bash
docker-compose up
```

Feel free to scale up the workers,

```bash
docker-compose scale worker=2
```