drop table if exists users;
create table users (
	id integer primary key autoincrement,
	user text not null unique,
	pass text not null unique,
	name text not null unique
);
drop table if exists entries;
create table entries (
	id integer primary key autoincrement,
	title text not null unique,
	author text not null,
	content text not null,
	foreign key(author) references users(name)
);