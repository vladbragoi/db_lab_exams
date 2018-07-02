from flask import Flask, request
from flask.templating import render_template
import psycopg2.extras

app = Flask(__name__)
_username = "postgres"
_password = "postgres"
_db_con = psycopg2.connect(host="localhost", database="esami", user=_username, password=_password)
_db_con.set_session(autocommit=True)


def _get_cursor():
    return _db_con.cursor(cursor_factory=psycopg2.extras.DictCursor)


def _get_voli():
    with _get_cursor() as cur:
        cur.execute("""
        SELECT iataCompagnia as iata, numeroVolo as num, orarioPartenza as ora
        FROM Volo
        """)
        return list(cur)


def _insert_business(numeroVolo, iataCompagnia, orarioVolo, codiceFiscale):
    with _get_cursor() as cur:
        try:
            cur.execute("""
                UPDATE Volo SET postiBusinessComprati = postiBusinessComprati + 1
                WHERE iataCompagnia = %s 
                  AND numeroVolo = %s
                  AND orarioPartenza = %s""", (iataCompagnia, numeroVolo, orarioVolo))
        except (Exception, psycopg2.IntegrityError):
            return False

    with _get_cursor() as cur:
        try:
            cur.execute("INSERT INTO Cliente VALUES (%s)", (codiceFiscale,))
        except (Exception, psycopg2.IntegrityError):
            return False
    with _get_cursor() as cur:
        try:
            cur.execute("INSERT INTO Prenotazione VALUES(%s, %s, %s, %s, %s)",
                        (iataCompagnia, numeroVolo, orarioVolo, codiceFiscale, True))
        except (Exception, psycopg2.IntegrityError):
            return False
    return True


def _insert_economy(numeroVolo, iataCompagnia, orarioVolo, codiceFiscale):
    with _get_cursor() as cur:
        try:
            cur.execute("""
                UPDATE Volo SET postiEconomyComprati = postiEconomyComprati + 1
                WHERE iataCompagnia = %s 
                  AND numeroVolo = %s
                  AND orarioPartenza = %s""", (iataCompagnia, numeroVolo, orarioVolo))
        except (Exception, psycopg2.IntegrityError):
            return False

    with _get_cursor() as cur:
        try:
            cur.execute("INSERT INTO Cliente VALUES (%s)", (codiceFiscale,))
        except (Exception, psycopg2.IntegrityError):
            return False

    with _get_cursor() as cur:
        try:
            cur.execute("INSERT INTO Prenotazione VALUES(%s, %s, %s, %s, %s)",
                        (iataCompagnia, numeroVolo, orarioVolo, codiceFiscale, False))
        except (Exception, psycopg2.IntegrityError):
            return False
    return True


@app.route('/')
def main():
    return render_template("index.html", voli=_get_voli())


@app.route('/prenota')
def prenota():
    nome = request.args['nome']
    codiceFiscale = request.args['cf']
    iataCompagnia, numeroVolo, orarioVolo = request.args['volo'].split(',')
    isBusiness = 'business' in request.args
    status = False

    if isBusiness:
        status = _insert_business(numeroVolo, iataCompagnia, orarioVolo, codiceFiscale)
    else:
        status = _insert_economy(numeroVolo, iataCompagnia, orarioVolo, codiceFiscale)

    if status:
        return render_template("prenotazioneEffettuata.html", nome=nome)
    else:
        return render_template("postiEsauriti.html", nome=nome)


def create_tb_database():
    with _get_cursor() as cur:
        cur.execute('''DROP TABLE IF EXISTS Cliente''')
        cur.execute('''DROP TABLE IF EXISTS Aeroporto''')
        cur.execute('''DROP TABLE IF EXISTS Compagnia''')
        cur.execute('''DROP TABLE IF EXISTS Volo''')
        cur.execute('''DROP TABLE IF EXISTS Prenotazione''')
        cur.execute('''CREATE TABLE Cliente(
                                    codiceFiscale VARCHAR(16) check (
                                        codiceFiscale SIMILAR TO
                                            '[A-Z]{6}\d{2}[A-Z]{1}\d{2}[A-Z]{1}\d{3}[A-Z]{1}'
                                    ) PRIMARY KEY        
                                )''')
        cur.execute('''CREATE TABLE Aeroporto(
                                    iata VARCHAR(4) PRIMARY KEY,
                                    nome VARCHAR(30)
                                )''')
        cur.execute('''CREATE TABLE Compagnia(
                                    icao VARCHAR(4) PRIMARY KEY
                                )''')
        cur.execute('''CREATE TABLE Volo(
                                    iataCompagnia VARCHAR(4),
                                    numeroVolo INTEGER,
                                    orarioPartenza TIME WITH TIME ZONE,
                                    postiBusiness INTEGER check (postiBusiness >= 0),
                                    postiEconomy INTEGER check (postiEconomy >= 0),
                                    postiBusinessComprati INTEGER check (
                                        postiBusinessComprati >= 0
                                        AND postiBusinessComprati <= postiBusiness
                                    ),
                                    postiEconomyComprati INTEGER check ( 
                                        postiEconomyComprati >= 0
                                        AND postiEconomyComprati <= postiEconomy
                                    ),
                                    PRIMARY KEY(iataCompagnia, numeroVolo, orarioPartenza),
                                    FOREIGN KEY(iataCompagnia) REFERENCES Compagnia(icao)        
                                )''')
        cur.execute('''CREATE TABLE Prenotazione(
                                    iataCompagnia VARCHAR(4),
                                    numeroVolo INTEGER,
                                    orarioPartenza TIME WITH TIME ZONE,
                                    codiceFiscale VARCHAR(16),
                                    isBusiness BOOLEAN,
                                    PRIMARY KEY(iataCompagnia, numeroVolo, orarioPartenza, codiceFiscale),
                                    FOREIGN KEY(iataCompagnia, numeroVolo, orarioPartenza) 
                                        REFERENCES Volo(iataCompagnia, numeroVolo, orarioPartenza),
                                    FOREIGN KEY(codiceFiscale) REFERENCES Cliente(codiceFiscale)
                                )''')
        cur.execute('''INSERT INTO Cliente VALUES('AAAAAA72B23Z152N')''')
        cur.execute('''INSERT INTO Aeroporto VALUES('AB34', 'Aeroporto1')''')
        cur.execute('''INSERT INTO Compagnia VALUES('COMP')''')
        cur.execute('''INSERT INTO Volo VALUES('COMP', 1, '14:00:00+01', 10, 100, 2, 50)''')
        cur.execute('''INSERT INTO Prenotazione VALUES('COMP', 1, '14:00:00+01', 'AAAAAA72B23Z152N', TRUE)''')


if __name__ == "__main__":
    # create_tb_database()
    app.run(debug=True)
