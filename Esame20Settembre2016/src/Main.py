import psycopg2.extras

_user = "postgres"
_password = "postgres"
_con = psycopg2.connect(host="localhost", database="esami", user=_user, password=_password)
_con.session(autocommit=True)


def _get_cursor():
    return _con.cursor(cursor_factory=psycopg2.extras.DictCursor)

def create_tables():
    with _get_cursor() as cur:
        cur.execute("""
            CREATE TABLE AUTOSTRADA (
              codice VARCHAR (5) PRIMARY KEY CHECK (codice SIMILAR TO 'A[0-9]+'),
              nome VARCHAR (50) UNIQUE NOT NULL ,
              gestore VARCHAR NOT NULL ,
              lunghezza NUMERIC (6 ,3) NOT NULL CHECK ( lunghezza > 0) -- in km con precisione al metro
            );
            CREATE TABLE COMUNE (
              codiceIstat CHAR (6) PRIMARY KEY CHECK ( SUBSTRING ( codiceIstat ,1 ,1) >= '0 ' AND
              SUBSTRING ( codiceIstat ,1 ,1) <= '9 ' AND ... -- si ripete per le altre posizioni
              -- un controllo migliore è CHECK ( SIMILAR TO '[0 -9]{6} ')
              nome VARCHAR (50) UNIQUE NOT NULL ,
              numeroAbitanti INTEGER NOT NULL CHECK ( numeroAbitanti >=0) ,
              superficie NUMERIC NOT NULL CHECK ( superficie > 0) -- in km quadrati
            );
            CREATE TABLE RAGGIUNGE (
              autostrada VARCHAR (5) REFERENCES AUTOSTRADA , -- non specificando ON UPDATE / DELETE , si pone la restrizione maggiore .
              comune CHAR (6) REFERENCES COMUNE ,
              numeroCaselli INTEGER NOT NULL CHECK ( numeroCaselli >=0) ,
              PRIMARY KEY ( autostrada , comune )
            );
        """)
        cur.execute("""SELECT * FROM AUTOSTRADA""")


if __name__ == "__main__":
    create_tables()