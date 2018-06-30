
drop table if exists auto;
create table auto(
	targa char(7) primary key check (targa SIMILAR TO '[A-Z]{2}[0-9]{3}[A-Z]{2}'),
	marca varchar(20) not null,
	modello varchar(30) not null,
	posti integer not null check (posti > 0) default 5,
	cilindrata integer not null check(cilindrata > 0)
);

drop table if exists cliente;
create table cliente(
	nPatente char(10) primary key,
	cognome varchar not null,
	nome varchar not null,
	paeseProvenienza varchar not null default 'Italia',
	nInfrazioni integer default 0 check(nInfrazione >= 0)
);

drop table if exists noleggio;
create table noleggio(
	targa char(7) references auto,
	cliente char(10) references cliente,
	inizio timestamp with time zone default current_timestamp,
	fine timestamp with time zone check(fine > inizio or fine is null),
	primary key (targa, cliente, inizio)
);

INSERT INTO auto (targa, marca, modello, posti, cilindrata)
	VALUES ('BE744FG', 'Ford', 'Ka', 5, 900),
		('CH131TN', 'Ford', 'Focus', 6, 1000),
		('ES500AS', 'KIA', 'Sportage', 6, 1000),
		('JF345DJ', 'Toyota', 'Aygo', 5, 1000),
		('JN456DF', 'Toyota', 'Yaris', 5, 950);

INSERT INTO cliente (nPatente, cognome, nome, paeseProvenienza, nInfrazioni)
	VALUES ('IT12345678', 'Danzi', 'Matteo', 'Italia', 0),
		('IT19876543', 'Danzi', 'Nicolo', 'Italia', 0),
		('IT26565432', 'Lennon', 'Giovanni', 'Italia', 2),
		('EN78965432', 'Jolie', 'Angelina', 'Inghilterra', 1);

INSERT INTO noleggio(targa, cliente, inizio, fine)
	VALUES ('ES500AS', 'IT19876543', '2016-03-11 00:00:00 CET', '2016-03-11 05:00:00 CET'),
		('CH131TN', 'IT12345678', '2017-03-11 14:00:00 CET', '2017-03-11 19:00:00 CET'),
		('BE744FG', 'IT26565432', '2017-02-20 13:00:00 CET', '2017-02-20 18:00:00 CET'),
		('BE744FG', 'EN78965432', '2017-01-12 00:30:00 CET', '2017-01-12 05:30:00 CET'),
		('CH131TN', 'IT12345678', '2017-04-11 14:00:00 CET', '2017-04-11 19:00:00 CET');