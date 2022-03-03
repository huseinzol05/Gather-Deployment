# Practice-PyFlink

Gathers data science and machine learning problem solving using PyFlink.

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

3. Build image,

```bash
docker build -t flink flink
```

4. Run docker compose,

```bash
docker-compose up -d
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