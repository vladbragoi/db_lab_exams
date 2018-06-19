drop domain if exists regioniItaliane;
create domain regioniItaliane as varchar(21)
	check(value in ('Trentino-Alto Adige' , 'Veneto' , 'Basilicata' , 'Puglia' ,'Molise' , 'Marche' , 'Umbria', 'Emilia-Romagna', 'Friuli-Venezia Giulia', 'Liguria' , 
					'Lombardia'  , 'Lazio'  , 'Campania' , 'Sicilia'  , 'Sardegna' , 'Toscana', 'Piemonte', 'Valle d aosta', 'Abruzzo', 'Calabria'));


drop table if exists ospedale;
create table ospedale(
	id integer primary key,
	nome varchar not null default 'Azienda Ospedaliera integrata ULSS22 Legnago'
);

drop table if exists divisione;
create table DIVISIONE(
	id integer primary key, 
	idOspedale integer not null references ospedale(id), 
	nome varchar not null , 
	numeroAddetti integer not null default 1 check(numeroAddetti>0)
	);

drop table if exists paziente;
create table PAZIENTE(
	codiceFiscale char(16) primary key check (codiceFiscale similar to '[a-zA-Z]{6}[0-9]{2}[a-zA-Z]{1}[0-9]{2}[a-zA-Z]{1}[0-9]{3}[a-zA-Z]{1}'), 
	nome varchar not null default 'Mario', 
	cognome varchar not null default 'Rossi', 
	regione regioniItaliane not null default 'Veneto', 
	nazione char(3) not null default 'ITA'
	);

drop table if exists RICOVERO;
create table RICOVERO(
	divisione integer references divisione(id), 
	paziente char(16) references paziente(codiceFiscale), 
	descrizione varchar not null, 
	urgenza varchar(20) not null, 
	dataAmmissione date not null, 
	dataDimissione date not null,
		PRIMARY KEY(divisione, paziente, dataAmmissione, dataDimissione)
	); 

INSERT INTO OSPEDALE(id, nome)
	VALUES (10, 'San Raffaele'), 
	(11, 'Policlinico Gemelli'), 
	(12, 'Policlinico Borgo Roma'), 
	(13, 'Ospedale Borgo Venezia'),
	(14, 'Fate Bene Fratelli'), 
	(15, 'Policlinico Borgo Milano'), 
	(16, 'Borgo Trento');

INSERT INTO DIVISIONE(id, idOspedale, nome, numeroAddetti)
	VALUES (01, 10, 'Ginecologia', 17), (02, 10, 'Pneumologia', 15), 
		(03, 16, 'Cardiochirurgia', 20), (04, 13, 'Podologia', 10),
		(05, 14, 'Reumatologia', 17), (06, 15, 'Neurochirurgia', 14), 
		(07, 14, 'Psichiatria', 18), (08, 12, 'Chirurgia Plastica', 10),
		(09, 12, 'Ostetricia', 20), (10, 12, 'Malattie Infettive', 20), 
		(11, 12, 'Ortopedia', 10), (12, 13, 'Pediatria', 19),
		(13, 16, 'Pediatria', 25);

INSERT INTO PAZIENTE (codiceFiscale, nome, cognome, regione, nazione)
	VALUES ('asdfun55c15u120g', 'giovanni', 'galli', 'Lazio', 'ITA'),
		   ('aseoij34u12q101r', 'carlo', 'conti', 'Toscana', 'CHE'),
		   ('pokfgj76p18d405s', 'silvia', 'giacometti', 'Veneto', 'ITA'),
		   ('pokasd89e12t309n', 'luca', 'coglione', 'Toscana', 'ITA'),
		   ('qwerty00o10s406f', 'greta', 'figa', 'Piemonte' ,'CHE'),
		   ('mnbvcx99k30h500f', 'giulia', 'roberts', 'Toscana', 'USA');

INSERT INTO RICOVERO(divisione, paziente, descrizione, urgenza, dataAmmissione, dataDimissione)
	VALUES (03, 'asdfun55c15u120g', 'colpo al cuore', 'Urgente', '2017-08-06', '2017-05-05'),
	(07, 'qwerty00o10s406f', 'impazzita', 'Non urgente', '2017-06-11', '2017-09-12'),
	(08, 'mnbvcx99k30h500f', 'rifacimento del naso', 'Trascurabile', '2017-06-06', '2017-06-07'),
	(02, 'aseoij34u12q101r', 'bronco polmonite', 'Urgente', '2017-06-06', '2017-07-07'),
	(03, 'pokasd89e12t309n', 'cuore di pietra', 'codice bianco', '2017-06-19', '2017-09-09'),
	(11, 'pokfgj76p18d405s', 'appendicite', 'Urgente', '2017-03-11', '2017-03-15'),
	(03, 'qwerty00o10s406f', 'piede a banana', 'No problem', '2017-03-19', '2017-03-21');
