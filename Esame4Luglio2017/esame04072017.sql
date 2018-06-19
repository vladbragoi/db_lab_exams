 create table biblioteca(
 	id integer primary key
 	);

 insert into biblioteca(id) values (207),(513),(336);

create domain tipoStato as varchar 
	check(value in ('abilitato','ammonito','sospeso'));

 create table UTENTE(
 	codiceFiscale  char(16) check(codiceFiscale similar to ('[A-Z]{6}[0-9]{2}[A-Z][0-9]{2}[A-Z][0-9]{3}[A-Z]')) primary key, 
 	nome varchar not null, 
 	cognome varchar not null, 
 	telefono char(11) check(telefono similar to ('+[0-9]{10}')) , 
 	dataIscrizione date not null default current_date, 
 	stato tipoStato not null
 	);
create table tipoRisorsa(
	tipo varchar primary key
);

insert into tipoRisorsa(tipo) values ('articolo', 'libro');

create domain tipoStatoRisorsa as varchar 
	check(value in ('solo consultazione' , 'disponibile' , 'on-line'));

create table RISORSA(
	id integer, 
	biblioteca integer references biblioteca(id), 
	titolo varchar not null, 
	tipo varchar not null references tipoRisorsa(tipo), 
	stato tipoStatoRisorsa not null,
	primary key(id, biblioteca)
	);

create table PRESTITO(
	idRisorsa integer, 
	idBiblioteca integer, 
	idUtente char(16), 
	dataInizio date default current_date, 
	durata interval,
	primary key (idRisorsa, idBiblioteca, idUtente, dataInizio),
	foreign key (idRisorsa, idBiblioteca) references RISORSA(id, biblioteca)
	);
