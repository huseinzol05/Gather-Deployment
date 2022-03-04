create table if not exists employee (id int, name text, last_update timestamp, last_comment text,
time_created timestamp default now(), PRIMARY KEY (id));
create table if not exists salary (id int, salary float, PRIMARY KEY (id));
insert into employee values (1, 'husein', now(), 'haram jadah betui');
update employee set last_update = now() where id = 1;
insert into employee values(2, 'kasim', now(), 'saya suka kerja disini');
insert into salary values (1, 100.0);
insert into salary values (2, 100.0);
update salary set salary = 1000.0;