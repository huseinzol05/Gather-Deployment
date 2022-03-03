# Practice-Pyspark

Gathers data science and machine learning problem solving using PySpark, Hadoop, Hive Metastore, Delta Lake, PySpark ML and PySpark NLP.

<img src="https://cdn-images-1.medium.com/max/1600/0*8D301fHKliN6r5Km.png" align="right" width="20%">

## Notebooks

1. Simple PySpark SQL, [sql.ipynb](notebook/1.sql.ipynb).

- Simple PySpark SQL.

2. Simple download dataframe from HDFS, [simple-hdfs.ipynb](notebook/2.simple-hdfs.ipynb). 

- Create PySpark DataFrame from HDFS.

3. Simple PySpark SQL with Hive Metastore, [simple-hive.ipynb](notebook/3.simple-hive.ipynb).

- Use PySpark SQL with Hive Metastore.

4. Simple Delta lake, [4.simple-delta-lake.ipynb](notebook/4.simple-delta-lake.ipynb).

- Simple Delta lake.

5. Delete Update Upsert using Delta, [5.delta-delete-update-upsert.ipynb](notebook/5.delta-delete-update-upsert.ipynb).

- Simple Delete Update Upsert using Delta lake.

6. Structured streaming using Delta, [6.delta-structured-streaming-data.ipynb](notebook/6.delta-structured-streaming-data.ipynb).

- Simple structured streaming with Upsert using Delta streaming.

7. Kafka Structured streaming using Delta, [7.kafka-structured-streaming-delta.ipynb](notebook/7.kafka-structured-streaming-delta.ipynb).

- Kafka structured streaming from PostgreSQL CDC using Debezium and Upsert using Delta streaming.

8. PySpark ML text classification, [8.text-classification.ipynb](notebook/8.text-classification.ipynb).

- Text classification using Logistic regression and multinomial in PySpark ML.

9. PySpark ML word vector, [9.word-vector.ipynb](notebook/9.word-vector.ipynb).

- Word vector in PySpark ML.

## How-to

1. Run HDFS and PostgreSQL for Hive Metastore,

```bash
docker container rm -f hdfs postgres
docker-compose -f misc.yaml up --build -d
```

2. Create Hive metastore in PostgreSQL,

```bash
PGPASSWORD=postgres docker exec -it postgres psql -U postgres -d postgres -c "$(cat hive-schema-3.1.0.postgres.sql)"
```

3. Run Kafka and Debezium for PostgreSQL CDC,

```bash
docker-compose -f kafka.yaml up
docker exec postgresql bash -c \
'PGPASSWORD=postgres psql -d postgres -U postgres -c "$(cat /bitnami/postgresql/conf/table.sql)"'
```

4. Add PostgreSQL CDC,

```bash
curl --location --request POST http://localhost:8083/connectors/ \
--header 'Content-Type: application/json' \
--data-raw '{
  "name": "employee-connector",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "tasks.max": "1",
    "plugin.name": "pgoutput",
    "database.hostname": "postgresql",
    "database.port": "5432",
    "database.user": "postgres",
    "database.password": "postgres",
    "database.dbname" : "postgres",
    "database.server.name": "employee",
    "key.converter": "org.apache.kafka.connect.json.JsonConverter",
    "key.converter.schemas.enable": "true",
    "table.whitelist": "public.employee,public.salary",
    "tombstones.on.delete": "false",
    "decimal.handling.mode": "double"
  }
}'
```

5. Build image,

```bash
docker build -t spark spark
```

6. Run docker compose,

```bash
docker-compose up -d
```

Feel free to scale up the workers,

```bash
docker-compose scale worker=2
```