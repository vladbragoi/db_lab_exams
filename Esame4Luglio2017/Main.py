from flask import Flask, request
from flask.templating import render_template
import psycopg2.extras

app = Flask(__name__)
_db_con = None
_user = "postgres"
_password = "postgres"

@app.route("/prestitiUtente")
def prestitiUtente():
    cf = ""
    id_bib = ""
    prestiti = None
    if request.method == 'GET':
        cf = request.args['cf'].strip()
        id_bib = request.args['bib'].strip()
    with _cursor() as cur:
        cur.execute("""SELECT idRisorsa as id, dataInizio as data, durata
                       FROM PRESTITO 
                       WHERE idBiblioteca = %s
                           AND idUtente = %s """, (id_bib, cf))
        prestiti = list(cur)
    if len(prestiti) == 0:
        return render_template('nessunPrestitoOErrore.html')
    return render_template('view.html', prestiti=prestiti)

@app.route("/")
def main():
    biblioteche=None
    with _cursor() as cur:
        cur.execute('''SELECT id, biblioteca
                       FROM RISORSA
                    ''')
        biblioteche = list(cur)
    return render_template('index.html', biblioteca=biblioteche)

def _cursor():
    return _db_con.cursor(cursor_factory=psycopg2.extras.DictCursor)

if __name__ == "__main__":
    _db_con = psycopg2.connect(host='localhost', database='esami', user=_user, password=_password)
    _db_con.set_session(autocommit=True)
    with _cursor() as cur:
        """
        cur.execute('''DROP TABLE IF EXISTS PRESTITO''')
        cur.execute('''DROP TABLE IF EXISTS RISORSA''')
        cur.execute('''DROP TABLE IF EXISTS UTENTE''')
        cur.execute('''CREATE TABLE RISORSA(
                            id INTEGER,
                            biblioteca VARCHAR(20),
                            titolo VARCHAR(30),
                            tipo VARCHAR(20),
                            stato VARCHAR(15),
                            PRIMARY KEY (id, biblioteca)                                 
                        )''')
        cur.execute('''CREATE TABLE UTENTE(
                            codiceFiscale VARCHAR(16) PRIMARY KEY,
                            nome VARCHAR(30),
                            cognome VARCHAR(30),
                            telefono VARCHAR(11),
                            dataIscrizione DATE,
                            stato VARCHAR(15)
                        )''')
        cur.execute('''CREATE TABLE PRESTITO(
                            idRisorsa INTEGER,
                            idBiblioteca VARCHAR(20),
                            idUtente VARCHAR(16),
                            dataInizio DATE,
                            durata INTERVAL,
                            PRIMARY KEY (idRisorsa, idBiblioteca, idUtente, dataInizio),
                            FOREIGN KEY (idRisorsa, idBiblioteca) REFERENCES RISORSA(id, biblioteca)
                            ON DELETE CASCADE
                        )''')
        cur.execute('''INSERT INTO RISORSA VALUES(0, 'Bruno Forte', 'Android Programming', 'Programming', 'disponibile')''')
        cur.execute('''INSERT INTO UTENTE VALUES('BRGVDS95B04Z140N', 'Vlad', 'Bragoi', '3925093287', '10/06/2018', 'abilitato')''')
        cur.execute('''INSERT INTO PRESTITO VALUES(0, 'Bruno Forte', 'BRGVDS95B04Z140N', '11/06/2018', '00:01:00')''')
        """
        pass

    app.run(debug=True)