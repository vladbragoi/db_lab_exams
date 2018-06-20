create table tipoContratto(
	tipo varchar primary key
);

create domain numero_telefono as varchar(10)
	check (value similar to '[0-9]{9,10}');
	
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
					(234, 'Bianchi', 'Francesco', '3473478795', 'vicolo Cieco', 1544),
					(345, 'Gino', 'DellaValle', '3886710619', 'via Masaglie', 1277);