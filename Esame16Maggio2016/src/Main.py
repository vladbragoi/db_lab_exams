#from flask import Flask, render_template
import psycopg2.extras

#app = Flask(__name__)
_username = "postgres"
_password = "postgres"
_con = psycopg2.connect(host="localhost", database="esami", user=_username, password=_password)
_con.set_session(autocommit=True)

def _get_cursor():
    return _con.cursor(cursor_factory=psycopg2.extras.DictCursor)

def create_tables():
    with _get_cursor() as cur:
        cur.execute("""
              drop table if exists auto cascade;
              create table auto(
                  targa char(7) primary key check (targa SIMILAR TO '[A-Z]{2}[0-9]{3}[A-Z]{2}'),
                  marca varchar(20) not null default 'Fiat',
                  modello varchar(30) not null default 'Panda',
                  posti integer not null check (posti > 0) default 5,
                  cilindrata integer not null check (cilindrata > 0) default 1200
              );
              
              drop table if exists cliente cascade;
              create table cliente(
                  nPatente char(10) primary key,
                  cognome varchar(30) not null default 'Rossi',
                  nome varchar(30) not null default 'Mario',
                  paeseProvenienza varchar(30) not null default 'Italia',
                  nInfrazioni integer default 0 check (nInfrazioni >= 0)
              );
    
              drop table if exists noleggio cascade;
              create table noleggio(
                  targa char(7) references auto(targa),
                  cliente char(10) references cliente(nPatente),
                  inizio timestamp with time zone default current_timestamp,
                  fine timestamp with time zone check(fine > inizio or fine is null),
                  primary key (targa, cliente, inizio)
              );
    
              INSERT INTO auto (targa, marca, modello, posti, cilindrata)
              VALUES ('BE744FG', 'Ford', 'Ka', 5, 900),
                  ('CH131TN', 'Ford', 'Focus', 6, 1000),
                  ('ES500AS', 'KIA', 'Sportage', 6, 1000),
                  ('JF345DJ', 'Toyota', 'Aygo', 5, 1000),
                  ('JN456DF', 'Toyota', 'Yaris', 5, 950);
    
              INSERT INTO cliente (nPatente, cognome, nome, paeseProvenienza, nInfrazioni)
              VALUES ('IT12345678', 'Danzi', 'Matteo', 'Italia', 0),
                  ('IT19876543', 'Danzi', 'Nicolo', 'Italia', 0),
                  ('IT26565432', 'Lennon', 'Giovanni', 'Italia', 2),
                  ('EN78965432', 'Jolie', 'Angelina', 'Inghilterra', 1);
    
              INSERT INTO noleggio(targa, cliente, inizio, fine)
              VALUES ('ES500AS', 'IT19876543', '2016-03-11 00:00:00 CET', '2016-03-11 05:00:00 CET'),
                  ('CH131TN', 'IT12345678', '2017-03-11 14:00:00 CET', '2017-03-11 19:00:00 CET'),
                  ('BE744FG', 'IT26565432', '2017-02-20 13:00:00 CET', '2017-02-20 18:00:00 CET'),
                  ('BE744FG', 'EN78965432', '2017-01-12 00:30:00 CET', '2017-01-12 05:30:00 CET'),
                  ('CH131TN', 'IT12345678', '2017-04-11 14:00:00 CET', '2017-04-11 19:00:00 CET');""")


if __name__ == "__main__":
    create_tables()

    marca = input("Inserire la marca dell'auto: ")

    with _get_cursor() as cur:
        cur.execute("""
            SELECT C1.nome, C1.cognome 
            FROM Cliente C1
            EXCEPT 
            SELECT C2.nome, C2.cognome
            FROM Cliente C2 JOIN Noleggio N ON N.cliente = C2.nPatente
                            JOIN Auto A ON A.targa = N.targa
            AND A.marca ILIKE %s""", (marca,))

        for row in cur:
            print(row)
    #app.run(debug=True)