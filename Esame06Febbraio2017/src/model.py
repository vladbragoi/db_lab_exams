import psycopg2.extras
from datetime import datetime, timedelta

_user = "postgres"
_password = "postgres"
_con = psycopg2.connect(host="localhost", database="esami", user=_user, password=_password)
_con.autocommit=True

def get_cursor():
    return _con.cursor(cursor_factory=psycopg2.extras.DictCursor)


def create_tables():
    with get_cursor() as cur:
        cur.execute("""
            drop table if exists tipoContratto cascade;
            create table tipoContratto(
	            tipo varchar primary key
            );

            drop domain if exists numeroTelefono cascade;
            create domain numeroTelefono as varchar(10)
	            check (value similar to '[0-9]{9,10}');
	
            insert into tipoContratto (tipo) values ('privato'),('business'),('corporate');

            drop table if exists citta cascade ;
            create table CITTA(
	            codice integer primary key, 
	            nome varchar(30) not null 
	        );

            drop table if exists cliente cascade;
            create table CLIENTE(
                codice integer primary key, 
                nome varchar not null, 
                cognome varchar not null, 
                nTelefono numero_telefono not null, 
                indirizzo varchar not null, 
                citta integer not null references CITTA on delete cascade
            );
            
            drop table if exists contratto cascade;
            create table CONTRATTO(
                contratto integer primary key,
                cliente integer not null references cliente(codice) on delete cascade, 
                tipo varchar not null default 'privato' references tipoContratto(tipo) on delete cascade, 
                dataInizio date not null default current_date, 
                dataFine date,
                check (dataFine > dataInizio)
            );
            
            drop table if exists telefonata cascade;
            create table TELEFONATA(
                contratto integer references contratto(contratto) on delete cascade, 
                nTelChiamato numeroTelefono, 
                istanteInizio timestamp,
                durata interval not null,
                primary key(contratto, nTelChiamato, istanteInizio)
            );

            insert into CITTA(codice, nome) values (1377, 'Padova'), (1544, 'Verona'), (1277, 'Vicenza');
            insert into CLIENTE(codice, nome, cognome, nTelefono, indirizzo, citta) 
                values(123, 'Mario', 'Rossi', '3886491850', 'via delle Passere', 1377),
                      (234, 'Bianchi', 'Francesco', '3473478795', 'vicolo Cieco', 1544),
                      (345, 'Gino', 'DellaValle', '3886710619', 'via Masaglie', 1277);
            insert into CONTRATTO(contratto, cliente, tipo, dataInizio, dataFine)
                values(1562, 123, 'privato', '2016-06-02', NULL),
                      (1572, 234, 'business', '2018-06-12', NULL),
                      (1582, 345, 'corporate', '2018-01-01', NULL);
            insert into TELEFONATA(contratto, nTelChiamato, istanteInizio, durata)
                values(1562, '3886491850', '2019-06-21 23:00', '1 minute 32 seconds'),
                      (1572, '3886710619', '2017-06-28 23:01', '00:05:20'::interval),
                      (1582,'3473478795','2016-06-20','10 minute 45 seconds');""")


def get_citta():
    with get_cursor() as cur:
        cur.execute("""SELECT codice, nome FROM CITTA""")
        return list(cur)


def Clienti(citta, data):
    data = datetime.strptime(data, "%Y-%m-%d")
    with get_cursor() as cur:
        cur.execute("""
            SELECT CL.nome, CL.cognome
            FROM CLIENTE CL 
                JOIN CONTRATTO C ON C.cliente = CL.codice
                JOIN TELEFONATA T ON T.contratto = C.contratto
            WHERE CL.citta = %s 
                AND T.istanteInizio::date = %s
        """, (citta, datetime.date(data)))
        return list(cur)