## how-to

1. Run mysql,

```bash
docker run --name mysql -e MYSQL_ROOT_PASSWORD=mysql -p3306:3306 mysql:5.6
```

2. Insert some tables,

```bash
docker exec -it mysql bash
cd /home
apt update
apt install git -y
git clone https://github.com/datacharmer/test_db.git
cd test_db/
mysql --password=mysql < employees.sql
mysql --password=mysql -t < test_employees_md5.sql
```

```text
+----------------------+
| INFO                 |
+----------------------+
| TESTING INSTALLATION |
+----------------------+
+--------------+------------------+----------------------------------+
| table_name   | expected_records | expected_crc                     |
+--------------+------------------+----------------------------------+
| departments  |                9 | d1af5e170d2d1591d776d5638d71fc5f |
| dept_emp     |           331603 | ccf6fe516f990bdaa49713fc478701b7 |
| dept_manager |               24 | 8720e2f0853ac9096b689c14664f847e |
| employees    |           300024 | 4ec56ab5ba37218d187cf6ab09ce1aa1 |
| salaries     |          2844047 | fd220654e95aea1b169624ffe3fca934 |
| titles       |           443308 | bfa016c472df68e70a03facafa1bc0a8 |
+--------------+------------------+----------------------------------+
```

3. Run Postgres,

```bash
docker run --name postgres -e POSTGRES_PASSWORD=postgres -p5432:5432 postgres:11-alpine
```

4. Run SymmetricDB,

```bash
docker run -p 31415:31415 --name sym jumpmind/symmetricds-pro
```

5. Create network

```bash
docker network create symdb-network
docker network connect symdb-network sym
docker network connect symdb-network postgres
docker network connect symdb-network mysql
```