import psycopg2.extras
from functools import reduce

_user = "postgres"
_password = "postgres"
_con = psycopg2.connect(host="localhost", database="esami", user=_user, password=_password)
_con.set_session(autocommit=True)


def _get_cursor():
    return _con.cursor(cursor_factory=psycopg2.extras.DictCursor)


def create_tables():
    with _get_cursor() as cur:
        cur.execute("""
            DROP TABLE IF EXISTS AUTOSTRADA CASCADE;
            CREATE TABLE AUTOSTRADA (
              codice VARCHAR (5) PRIMARY KEY CHECK (codice SIMILAR TO 'A[0-9]+'),
              nome VARCHAR (50) UNIQUE NOT NULL ,
              gestore VARCHAR NOT NULL ,
              lunghezza NUMERIC (6 ,3) NOT NULL CHECK ( lunghezza > 0) -- in km con precisione al metro
            );
            
            DROP TABLE IF EXISTS COMUNE CASCADE;
            CREATE TABLE COMUNE (
              codiceIstat CHAR (6) PRIMARY KEY CHECK (codiceIstat SIMILAR TO '[0 -9]{6}'),
              nome VARCHAR (50) UNIQUE NOT NULL,
              numeroAbitanti INTEGER NOT NULL CHECK ( numeroAbitanti >=0) ,
              superficie NUMERIC NOT NULL CHECK ( superficie > 0) -- in km quadrati
            );
            
            DROP TABLE IF EXISTS RAGGIUNGE CASCADE;
            CREATE TABLE RAGGIUNGE (
              autostrada VARCHAR (5) REFERENCES AUTOSTRADA ON DELETE CASCADE,
              comune CHAR (6) REFERENCES COMUNE ON DELETE CASCADE ,
              numeroCaselli INTEGER NOT NULL CHECK ( numeroCaselli >=0) ,
              PRIMARY KEY ( autostrada , comune )
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
                VALUES ('A1', '123456', 4), ('A1', '123454', 2), ('A1', '123452', 4), ('A1', '123453', 6), 
                ('A1', '123451', 2), ('A1', '123450', 1), ('A1', '123457', 2), ('A2', '123459', 4), 
                ('A2', '123458', 4), ('A2', '123457', 4), ('A2', '123456', 4), ('A3', '123452', 4), 
                ('A3', '123451', 4), ('A3', '123454', 4), ('A4', '123450',1);
          """)

def get_autostrade():
    with _get_cursor() as cur:
        cur.execute("""
            SELECT codice
            FROM AUTOSTRADA
        """)
        return list(cur)

def get_comuni():
    with _get_cursor() as cur:
        cur.execute("""
            SELECT codiceIstat, nome
            FROM COMUNE
        """)
        return list(cur)

def insert_tuple(autostrada, comune, caselli):
    with _get_cursor() as cur:
        cur.execute("""
            INSERT INTO RAGGIUNGE
            VALUES (%s, %s, %s)""", (autostrada, comune, caselli))

if __name__ == "__main__":
    create_tables()
    autostrade = None
    comuni = None
    autostrada = ""
    comune = ""

    while (input("Vuoi inserire una nuova tupla? [S/N]: ").lower() == "S".lower()):
        print("Inserisci un'autostrada tra queste: ")
        autostrade = reduce(lambda x, y : x + y ,get_autostrade())
        print(autostrade)
        while autostrada not in autostrade:
            autostrada = input("> ")

        print("Inserisci un comune tra questi: ")

        comuni = reduce(lambda x, y : x + y ,get_comuni())
        print(comuni)
        while comune not in comuni:
            comune = input("> ")

        caselli = int(input("Inserisci il numero di caselli: "))
        if isinstance(caselli, int):
            try:
                insert_tuple(autostrada, comune, caselli)
            except (Exception, psycopg2.IntegrityError):
                print("Errore di integrità. Riprovare.")
            autostrada = ""
            comune = ""