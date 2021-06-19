## How-to

1. Run docker compose,

```bash
docker-compose docker-compose.yaml up --build
```

2. Access Hive beeline and create database,

```bash
docker exec -it hive bash
$HIVE_HOME/bin/beeline  -u jdbc:hive2://localhost:10000 -n root -p hive -f test.hql
```

