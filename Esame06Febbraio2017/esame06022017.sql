--Si consideri il seguente schema relazionale parziale 
--(chiavi primarie sottolineate) contenente le informazioni relative 
--alla programmazione di allenamenti:
--dove entrambi gli attributi livello hanno dominio 
--{principiante, intermedio, avanzato}, gruppoMuscolare ha dominio 
--GM={petto, schiena, spalle, braccia, gambe}, giorno è il nome del giorno
-- della settimana, ordine è un intero che indica l’ordine di esecuzione 
--in un allenamento, serie indica quante volte una serie di ripetizioni 
--deve essere svolta, ripetizioni indica quante volte un esercizio deve
-- essere ripetuto, TUT è il tempo sotto tensione in s, che viene 
--rappresentato come 4 valori interi distinti e riposo è il tempo in s
-- di riposo tra una serie e la successiva.
--Si sottolinea che un PROGRAMMA è composto da un insieme di esercizi
--distribuiti su uno o più giorni.
--Domanda 1 [5 punti]
--Scrivere in codice PostgreSQL la dichiarazione di tutti i domini 
--necessari per implementare lo schema relazionale.
--Scrivere una tabella che rappresenti i possibili valori di TUT: 
--ciascuna tupla deve rappresentare un id e una possibile combinazione 
--di 4 interi non negativi.
--Scrivere il codice PostgreSQL che generi le tabelle per rappresentare
-- lo schema relazionale con tutti i possibili controlli di integrità e 
--di correttezza dei dati.

create domain dLivello as varchar
	check(value in ('principiante','intermedio','avanzato'));
create domain GM as varchar
	check(value in ('petto', 'schiena', 'spalle', 'braccia', 'gambe'));
CREATE DOMAIN giorniSettimana AS CHAR(3)
	CHECK( VALUE IN('LUN', 'MAR', 'MER', 'GIO', 'VEN', 'SAB', 'DOM') );


CREATE TABLE TUT (
id VARCHAR PRIMARY KEY ,
eccentrico INTEGER NOT NULL CHECK(eccentrico >=0),
stopEcc INTEGER NOT NULL CHECK(stopEcc >=0), 
concentrico INTEGER NOT NULL CHECK(concentrico >=0), 
stopCon INTEGER NOT NULL CHECK(stopCon >=0)
);


CREATE TABLE ESERCIZIO (
nome VARCHAR PRIMARY KEY , 
livello dLivello NOT NULL , 
gruppo GM NOT NULL
);

CREATE TABLE PROGRAMMA (
nome VARCHAR PRIMARY KEY ,
livello dLivello NOT NULL 
);

CREATE TABLE ESERCIZIO_IN_PROGRAMMA(
nomeProgramma VARCHAR REFERENCES PROGRAMMA,
giorno giorniSettimana not null,
nomeEsercizio VARCHAR REFERENCES ESERCIZIO,
serie INTEGER NOT NULL CHECK (serie > 0),
ripetizioni INTEGER NOT NULL CHECK (ripetizioni > 0),
ordine  INTEGER NOT NULL CHECK (ordine > 0),
tut VARCHAR REFERENCES TUT NOT NULL ,
riposo INTEGER NOT NULL CHECK (riposo >=0),--in s
PRIMARY KEY (nomeprogramma , giorno , nomeesercizio) 
);



INSERT INTO TUT(id, eccentrico, stopEcc, concentrico, stopCon)
	VALUES ( 'abc', 3, 4, 5, 6 ), ('bbc', 1, 2, 3, 4), ('cbc', 4, 5, 6, 7), ('dbc', 5, 6, 7, 8), ('ebc', 6, 7, 8, 9);

INSERT INTO ESERCIZIO(nome, livello, gruppo)
	VALUES ('panca piana', 'intermedio', 'petto'), ('vogatore', 'intermedio', 'braccia'), ('butterfly', 'principiante', 'petto'),
		('pressa', 'principiante', 'gambe'), ('lat machine', 'principiante', 'schiena'), ('shoulder press', 'intermedio', 'spalle'),
		('leg press', 'principiante', 'gambe');

INSERT INTO PROGRAMMA(nome, livello)
	VALUES ('full body', 'principiante'), ('three days', 'intermedio'), ('extreme workout', 'avanzato'), ('soft workout', 'principiante');

INSERT INTO ESERCIZIO_IN_PROGRAMMA(nomeProgramma, giorno, nomeEsercizio, ordine, serie, ripetizioni, tut, riposo)
	VALUES ('full body', 'LUN', 'butterfly', 2, 3, 10, 'bbc', 2),
		('full body', 'GIO', 'lat machine', 1, 3, 10, 'abc', 2),
		('full body', 'LUN', 'vogatore', 1, 3, 10 , 'abc', 2),
		('full body', 'VEN', 'lat machine', 1, 3, 10, 'abc', 2),
		('full body', 'LUN', 'leg press', 1, 3, 10 , 'abc', 2),
		('full body', 'MAR', 'lat machine', 1, 3, 10, 'abc', 2),
		('full body', 'MER', 'lat machine', 1, 3, 10 , 'abc', 2),
		('full body', 'SAB', 'lat machine', 1, 3, 10, 'abc', 2),
		('full body', 'MER', 'panca piana', 1, 3, 10 , 'abc', 2),
		('extreme workout', 'LUN', 'leg press', 1, 4, 20, 'ebc', 2),
		('extreme workout', 'LUN', 'pressa', 2, 3, 25, 'dbc', 2),
		('extreme workout', 'MER', 'panca piana', 1, 4, 20, 'cbc', 2),
		('extreme workout', 'VEN', 'pressa', 1, 3, 20, 'bbc', 2),
		('three days', 'LUN', 'pressa', 1, 4, 20, 'ebc', 2),
		('three days', 'DOM', 'lat machine', 1, 3, 10, 'abc', 2),
		('three days', 'VEN', 'butterfly', 2, 3, 15, 'abc', 2),
		('three days', 'VEN', 'shoulder press', 1, 3, 20, 'bbc', 2);