drop table if exists autostrada;
CREATE TABLE AUTOSTRADA (
codice VARCHAR(5) PRIMARY KEY CHECK (codice LIKE 'A%'), --meglio (SIMILAR TO'A[0-9]+'),
nome VARCHAR (50) UNIQUE NOT NULL,
gestore VARCHAR NOT NULL,
lunghezza NUMERIC(6,3) NOT NULL CHECK (lunghezza > 0) --in km con precisione al metro
);


drop table if exists comune;
CREATE TABLE COMUNE (
codiceIstat CHAR(6) PRIMARY KEY CHECK(codiceIstat SIMILAR to '[0-9]{6}'),
nome VARCHAR (50) UNIQUE NOT NULL ,
numeroAbitanti INTEGER NOT NULL CHECK (numeroAbitanti >=0),
superficie NUMERIC NOT NULL CHECK (superficie > 0) --in km quadrati
);

drop table if exists raggiunge;
CREATE TABLE RAGGIUNGE(
autostrada VARCHAR(5) REFERENCES AUTOSTRADA(codice) ,--non specificando ON UPDATE/DELETE , si pone la restrizione maggiore.
comune CHAR (6) REFERENCES COMUNE(codiceIstat) ,
numeroCaselli INTEGER NOT NULL CHECK (numeroCaselli >=0), 
	PRIMARY KEY(autostrada ,comune)
	);


INSERT INTO AUTOSTRADA(codice, nome, gestore, lunghezza)
	VALUES ('A1', 'a', '1', 100),
	('A2', 'b', '2', 500),
	('A3', 'c', '3', 510),
	('A4', 'd', '2', 520),
	('A5', 'e', '3', 530),
	('A6', 'f', '1', 550),
	('A7', 'g', '2', 540),
	('A8', 'h', '3', 560),
	('A9', 'u', '3', 570),
	('A10','l', '3', 580);

INSERT INTO COMUNE(codiceIstat, nome, numeroAbitanti, superficie)
	VALUES ('123456', 'Verona', 1200, 1000),
	('123457', 'Vicenza', 1300, 1050),
	('123458', 'Padova', 1400, 1045),
	('123459', 'Bologna', 1500, 4030),
	('123450', 'Venezia', 1600, 1020),
	('123451', 'Molveno', 1700, 100),
	('123452', 'Caldiero', 1800, 1000),
	('123453', 'Viterbo', 1900, 1060),
	('123454', 'Lucca', 1020, 3000);
	
INSERT INTO RAGGIUNGE(autostrada, comune, numeroCaselli)
	VALUES ('A1', '123456', 4),
	('A1', '123454', 2), ('A1', '123452', 4), ('A1', '123453', 6), ('A1', '123451', 2), ('A1', '123450', 1), ('A1', '123457', 2), 
	('A2', '123459', 4), ('A2', '123458', 4), ('A2', '123457', 4), ('A2', '123456', 4),
	('A3', '123452', 4), ('A3', '123451', 4), ('A3', '123454', 4),
	('A4', '123450',1);