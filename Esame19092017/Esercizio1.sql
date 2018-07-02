create domain IATAAeroporto as varchar(4) check(value similar to '[a-z][0-9]{2,3}');
create domain IATACompagnia as char(2) check(value similar to '[a-z][0-9]');
create domain ICAOCompagnia as char(4) check(value similar to '[a-z][0-9]{3}');

create table CLIENTE(
	codiceFiscale char(16) primary key check(codiceFiscale similar to '[a-z]{6}[0-9]{2}[a-z][0-9]{2}[a-z][0-9]{3}[a-z]'),
	nome varchar not null, 
	cognome varchar not null, 
	telefono char(11) not null check(telefono similar to '+[0-9]{10}'), 
	sesso char(1) not null check(sesso in ('M', 'F'))
	);
create table AEROPORTO(
	iata IATAAeroporto primary key, 
	nome varchar not null, 
	città varchar not null, 
	nazione varchar not null
	);
create table COMPAGNIA(
	icao ICAOCompagnia primary key unique, 
	iata IATACompagnia not null unique,
	nome varchar not null, 
	nazione varchar not null
	);

create table VOLO(
	iataCompagnia IATACompagnia references COMPAGNIA(iata), 
	numero integer check (numero > 0), 
	orarioPartenza timestamp with time zone , 
	icaoCompagnia ICAOCompagnia not null references COMPAGNIA(icao), 
	partenza IATAAeroporto not null references AEROPORTO, 
	destinazione IATAAeroporto not null references AEROPORTO,  
	durata interval not null check(durata > '00:00:00'::interval),
	postiBusiness integer not null check(postiBusiness >= 0), 
	postiEconomy integer not null check(postiEconomy >= 0), 
	postiBusinessComprati integer not null check(postiBusinessComprati >= 0 and postiBusinessComprati<= postiBusiness), 
	postiEconomyComprati integer not null check(postiEconomyComprati >= 0 and postiEconomyComprati <= postiEconomy),
		primary key(iataCompagnia, numero, orarioPartenza)
		);

create table PRENOTAZIONE(
	iataCompagnia IATACompagnia,
	 numeroVolo integer, 
	 orarioPartenza timestamp with time zone, 
	 codiceFiscale char(16) references CLIENTE, 
	 isBusiness boolean not null,
	 	primary key(iataCompagnia, numeroVolo, orarioPartenza, codiceFiscale),
	 	foreign key(iataCompagnia, numeroVolo, orarioPartenza) references VOLO(iataCompagnia, numero, orarioPartenza)
	 );