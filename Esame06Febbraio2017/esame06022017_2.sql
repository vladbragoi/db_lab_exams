create table tipoContratto(
	tipo varchar primary key
);

create domain numero_telefono as varchar(10)
	check (value similar to '[0-9]{10}');
	
insert into tipoContratto (tipo) values ('privato'),('business'),('corporate');

create table CITTA(
	codice integer primary key, 
	nome varchar(30) not null 
	);

create table CLIENTE(
	codice integer primary key, 
	nome varchar not null, 
	cognome varchar not null, 
	nTelefono numero_telefono not null, 
	indirizzo varchar not null, 
	citta integer not null references CITTA
	);

create table CONTRATTO(
	contratto integer primary key,
	cliente integer not null references cliente(codice), 
	tipo varchar references tipoContratto(tipo) not null default 'privato', 
	dataInizio date not null default current_date, 
	dataFine date,
	check (dataFine > dataInizio)
	);

create table TELEFONATA(
	contratto integer references contratto(contratto), 
	nTelChiamato numero_telefono, 
	instanteInizio timestamp,
	durata interval not null,
	primary key(contratto, nTelChiamato, instanteInizio)
	);


insert into CITTA(codice, nome) values (1377, 'Padova'), (1544, 'Verona'), (1277, 'Vicenza');
insert into CLIENTE(codice, nome, cognome, nTelefono, indirizzo, citta) 
			values(123, 'Mario', 'Rossi', '3886491850', 'via delle Passere', 1377),
					(235, 'Bianchi', 'Francesco', '3473478795', 'vicolo Cieco', 1544),
					(345, 'Gino', 'DellaValle', '3886710619', 'via Masaglie', 1277);
insert into contratto(contratto, cliente, tipo, dataInizio , dataFine) 
	values(1562, 123, 'privato', '2018-06-20', '2019-06-21'),
			(1572, 234, 'privato','2017-06-20', '2017-06-21'),
			(1582, 345, 'business', '2016-06-20', '2016-06-21');

insert into TELEFONATA(contratto, nTelChiamato, instanteInizio, durata)
	values(1562, '3886491850', '2019-06-21 23:00', '1 minute 32 seconds'),
			(1572, '3886710619', '2017-06-28 23:01', '00:05:20'::interval),
			(1582,'3473478795','2016-06-20','10 minute 45 seconds');


SELECT C.cognome, C.nome, C.indirizzo
FROM Cliente C JOIN CITTA CI ON C.citta=CI.codice 
JOIN Contratto CO ON C.codice=CO.cliente 
JOIN TELEFONATA T ON T.contratto=CO.contratto
WHERE CI.nome='Padova' AND t.instanteInizio >= CURRENT_DATE-1 AND t.instanteInizio < CURRENT_DATE
EXCEPT

SELECT C.cognome, C.nome, C.indirizzo
FROM Cliente C JOIN CITTA CI ON C.citta=CI.codice 
JOIN Contratto CO ON C.codice=CO.cliente 
JOIN TELEFONATA T ON T.contratto=CO.contratto
WHERE CI.nome='Padova' AND t.instanteInizio >= CURRENT_DATE - 1 + TIME '10:00' AND t.instanteInizio <= CURRENT_DATE - 1 + TIME '17:00';