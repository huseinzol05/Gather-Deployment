create table if not exists employee (id int, name text, last_update timestamp, 
time_created timestamp default now(), PRIMARY KEY (id));
insert into employee values (1, 'husein', now());
update employee set last_update = now() where id = 1;
insert into employee values(2, 'kasim', now());