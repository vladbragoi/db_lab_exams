create domain tipoConvegno as varchar
	check(value in ('seminario', 'simposio', 'conferenza'));

create table convegno (
	nome varchar(30) primary key,
	dataInizio date not null,
	dataFine date check(dataFine >= dataInizio),
	numeroSessioni integer not null check (numeroSessioni > 0),
	tipo tipoConvegno not null,
	luogo varchar not null 
);

create table intervento(
	id integer primary key,
	titolo varchar not null,
	relatore varchar not null,
	durata interval not null check(durata > '1 second'::interval)

);

create table sessione (
	nome varchar,
	nomeConvegno varchar(30) references convegno(nome),
	data date not null,
	orarioInizio timestamp with time zone not null,
	orarioFine timestamp with time zone not null check(orarioFine > orarioInizio),
	primary key(nome, nomeConvegno)
);
-- una sessione può durare più di un giorno;

create table intervento_in_convegno(
	nomeConvegno varchar(30) references convegno(nome),
	idIntervento integer references intervento(id),
	nomeSessione varchar,
	orarioInizio timestamp with time zone not null,
	foreign key(nomeSessione, nomeConvegno) references sessione(nome, nomeConvegno),
	primary key(nomeConvegno, idIntervento, nomeSessione)
);


insert into convegno(nome, dataInizio, dataFine, numeroSessioni, tipo, luogo)
 values	('Guittar Show', '2018-06-08', '2018-06-10', 3, 'conferenza', 'Padova'),
					('Polo Zanotto', '2018-06-19', '2018-06-21', 5, 'seminario', 'Verona'),
					('Tecnologie Industriali', '2017-09-16', '2018-09-16', 27, 'simposio', 'Marragnole');

insert into intervento(id, titolo, relatore, durata)
	values(1, 'Come cambiare le corde', 'Giovanni Boscaini', '01:10:19'::interval),
		(2, 'Come cambiare i pannolini', 'Cristian Sandu', '00:05:00'::interval),
		(3, 'Come montare una turbina', 'Leonardo Testolin', '01:30:00'::interval);
insert into sessione(nome, nomeConvegno, data, orarioInizio, orarioFine)
	values('Sessione 404', 'Tecnologie Industriali', '2017-09-16',  '20:50:00+01', '23:50:00+01');

insert into intervento_in_convegno(nomeConvegno,idIntervento, nomeSessione, orarioInizio)
	values('Tecnologie Industriali', 3, 'Sessione 404', '20:50:00+01');


INSERT INTO SESSIONE(nome,nomeConvegno,data,orarioInizio,orarioFine)
    VALUES
        ('Domanda1','Guittar Show','2010-06-19','11:51:50','11:51:59'),
        ('Domanda2','Tecnologie Industriali','2010-06-19','11:51:50','11:52:00'),
        ('Domande3','Guittar Show','2010-06-19','11:51:50','12:10:50');

INSERT INTO INTERVENTO_IN_CONVEGNO(nomeConvegno,idIntervento,nomeSessione,orarioInizio)
    VALUES
        ('Guittar Show',2,'Domanda1','10:51:50'),
        ('Tecnologie Industriali',1,'Domanda2','12:51:50'),
        ('Tecnologie Industriali',3,'Domanda2','16:51:50');

