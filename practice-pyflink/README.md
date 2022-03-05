# Practice-PyFlink

Gathers data science and machine learning problem solving using PyFlink.

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/Apache_Flink_logo.svg/1200px-Apache_Flink_logo.svg.png" align="right" width="20%">

## Notebooks

1. Simple Word Count to HDFS, [tableapi-word-count-hdfs.ipynb](notebook/1.tableapi-word-count-hdfs.ipynb).

- Simple Table API to do Word Count and sink into Parquet format in HDFS.

2. Simple Word Count to PostgreSQL, [tableapi-word-count-postgres.ipynb](notebook/2.tableapi-word-count-postgres.ipynb).

- Simple Table API to do Word Count and sink into PostgreSQL using JDBC.

3. Simple Word Count to Kafka, [tableapi-word-count-kafka.ipynb](notebook/3.tableapi-word-count-postgres.ipynb).

- Simple Table API to do Word Count and sink into Kafka.

4. Simple text classification to HDFS, [tableapi-malay-sentiment-classifer-hdfs.ipynb](notebook/4.tableapi-malay-sentiment-classifer-hdfs.ipynb).

- Load trained text classification model using UDF to classify sentiment and sink into Parquet format in HDFS.

5. Simple text classification to PostgreSQL, [tableapi-malay-sentiment-classifer-postgres.ipynb](notebook/5.tableapi-malay-sentiment-classifer-postgres.ipynb).

- Load trained text classification model using UDF to classify sentiment and sink into PostgreSQL.

6. Simple text classification to Kafka, [tableapi-malay-sentiment-classifer-kafka.ipynb](notebook/6.tableapi-malay-sentiment-classifer-kafka.ipynb).

- Load trained text classification model using UDF to classify sentiment and sink into Kafka.

7. Simple real time text classification upsert to PostgreSQL, [tableapi-malay-sentiment-classifer-kafka-upsert-postgres.ipynb](notebook/7.tableapi-malay-sentiment-classifer-kafka-upsert-postgres.ipynb).

- Simple real time text classification from Debezium CDC and upsert into PostgreSQL.

8. Simple real time text classification upsert to Kafka, [tableapi-malay-sentiment-classifer-kafka-upsert-kafka.ipynb](notebook/8.tableapi-malay-sentiment-classifer-kafka-upsert-kafka.ipynb).

- Simple real time text classification from Debezium CDC and upsert into Kafka Upsert.

## How-to

1. Run HDFS and PostgreSQL for Hive Metastore,

```bash
docker container rm -f hdfs postgres
docker-compose -f misc.yaml build
docker-compose -f misc.yaml up
```

2. Create Hive metastore in PostgreSQL,

```bash
PGPASSWORD=postgres docker exec -it postgres psql -U postgres -d postgres -c "$(cat hive-schema-3.1.0.postgres.sql)"
```

3. Build image,

```bash
docker build -t flink flink
```

4. Run docker compose,

```bash
docker-compose up
```

Feel free to scale up the workers,

```bash
docker-compose scale taskmanager=2
```

To access Flink SQL CLI,

```
docker exec -it flink /opt/flink/bin/sql-client.sh
```

4. Run Kafka and Debezium for PostgreSQL CDC,

```bash
docker-compose -f kafka.yaml up
docker exec postgresql bash -c \
'PGPASSWORD=postgres psql -d postgres -U postgres -c "$(cat /bitnami/postgresql/conf/table.sql)"'
```

5. Add PostgreSQL CDC,

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