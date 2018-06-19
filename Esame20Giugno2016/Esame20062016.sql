drop table if exists ingrediente;

create table INGREDIENTE(
	Id integer primary key, 
	Nome varchar not null default 'Acqua', 
	Calorie integer not null default 0 check (calorie >= 0) , 
	grassi DECIMAL NOT NULL default 0 CHECK(grassi >=0 AND grassi <=100),
	proteine DECIMAL NOT NULL default 0 CHECK(proteine >=0 AND proteine <=100),
	carboidrati DECIMAL NOT NULL default 0 CHECK(carboidrati >=0 AND carboidrati <=100)
	);

drop table if exists ricetta;
create table RICETTA(
	Id integer primary key, 
	Nome varchar not null default 'Pizza', 
	Regione varchar(30), 
	Porzioni integer not null default 2, 
	TempoPreparazione interval 
	);

drop table if exists COMPOSIZIONE;
create table COMPOSIZIONE(
	Ricetta integer references ricetta(id), 
	Ingrediente integer references ingrediente(id), 
	quantità DECIMAL(5,2) CHECK (quantità > 0),
	primary key(ricetta, ingrediente)
	);

INSERT INTO INGREDIENTE(id, nome, calorie, grassi, proteine, carboidrati)
	VALUES (1234, 'sale', 0, 12, 13, 30),
		(1235, 'pasta', 40, 20, 80, 50),
		(1236, 'pane', 20, 50, 50, 10),
		(1237, 'pomodoro', 20, 20, 10, 10),
		(1238, 'formaggio', 50, 50, 70, 70),
		(1239, 'cioccolato', 80, 80, 50, 10),
		(1240, 'salame', 60, 60, 60, 60);

INSERT INTO RICETTA(id, nome, regione, porzioni, tempoPreparazione)
	VALUES (1, 'pizza', 'Campania', 4, '1 hour'),
		(2, 'Pane e salame', 'Veneto', 4, '5 minutes'),
		(3, 'pasta al pomodoro', 'Veneto', 2, '20 minutes'),
		(4, 'Salame al cioccolato', 'Veneto', 2, '15 minutes 30 seconds');

INSERT INTO COMPOSIZIONE(ricetta, ingrediente, quantità)
	VALUES(1, 1234, 20),
		(1, 1237, 60),
		(1, 1238, 60),
		(2, 1236, 50),
		(2, 1240, 50),
		(3, 1235, 80),
		(3, 1234, 1),
		(3, 1237, 70),
		(4, 1236, 50),
		(4, 1239, 50);
		
select * from ricetta where tempopreparazione = '01:00:00'::INTERVAL;