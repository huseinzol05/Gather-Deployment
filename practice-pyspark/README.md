# Practice-Pyspark

Gathers data science and machine learning problem solving using PySpark, Hadoop, Hive Metastore, Delta Lake, PySpark ML and PySpark NLP.

<img src="https://cdn-images-1.medium.com/max/1600/0*8D301fHKliN6r5Km.png" align="right" width="20%">

## Notebooks

1. Simple PySpark SQL, [sql.ipynb](notebook/1.sql.ipynb).
2. Simple download dataframe from HDFS, [simple-hdfs.ipynb](notebook/2.simple-hdfs.ipynb). 
3. Simple PySpark SQL with Hive Metastore, [simple-hive.ipynb](notebook/3.simple-hive.ipynb).
4. Simple Delta lake, [4.simple-delta-lake.ipynb](notebook/4.simple-delta-lake.ipynb).
5. Delete Update Upsert using Delta, [5.delta-delete-update-upsert.ipynb](notebook/5.delta-delete-update-upsert.ipynb).
6. Structured streaming using Delta, [6.delta-structured-streaming-data.ipynb](notebook/6.delta-structured-streaming-data.ipynb).

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