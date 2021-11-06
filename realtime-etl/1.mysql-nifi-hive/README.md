## How-to

1. Run docker compose,

```bash
docker-compose docker-compose.yaml up --build
```

2. Access Hive beeline and create a simple database from parquets,

Below is optional, to make sure Hive able to use YARN for map reduce,

```bash
docker exec -it hive bash
$HIVE_HOME/bin/beeline  -u jdbc:thrift://hive:10000/default -n root -p hive -f test.hql
wget https://raw.githubusercontent.com/Teradata/kylo/master/samples/sample-data/parquet/userdata1.parquet
wget https://raw.githubusercontent.com/Teradata/kylo/master/samples/sample-data/parquet/userdata2.parquet
hdfs dfs -mkdir /user/users
hdfs dfs -put userdata1.parquet userdata2.parquet /user/users
$HIVE_HOME/bin/beeline  -u jdbc:hive2://hive:10000/default -n root -p hive
create external table users (registration_dttm timestamp, id int, first_name string, last_name string, email string, gender string, ip_address string, cc string, country string, birthdate string, salary double, title string, comments string) stored as parquet location '/user/users';
select * from users;
select country, count(id) from users group by country;
```

```bash
docker exec -it hive bash
hdfs dfs -mkdir /user/hive/users1
$HIVE_HOME/bin/beeline  -u jdbc:hive2://hive:10000/default -n root -p hive
create table users1(id int, last_update timestamp, name string) stored as parquet location '/user/users';
```

3. Create a table inside MySQL,

```bash
docker exec -it mysql bash
mysql --user=root --password=mysql --database=mysql
create table users(id int, last_update timestamp, name varchar(255), primary key (id));
insert into users values (1, now(), 'husein');
```





