drop table if exists tasks;
drop table if exists users;
drop table if exists statuses;

create table users (
id serial primary key,
fullname varchar(100),
email varchar(100) unique
);

create table statuses (
id serial primary key,
name varchar(50) unique
);

create table tasks (
id serial primary key,
title varchar(100),
description text,
status_id integer,
user_id integer,
constraint fk_user
	foreign key (user_id) 
		references users(id)
			on delete cascade,
constraint fk_status
	foreign key (status_id) 
		references statuses(id)
);

