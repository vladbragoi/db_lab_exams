'''Controller dell'applicazione web 'Insegnamenti'
Formattazione salva righe per i lucidi!
@author: posenato'''

import logging
from flask import Flask, request
from flask.templating import render_template
from Model import Model

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)  # Applicazione Flask!
app.jinja_env.line_statement_prefix = '#'  # attivo Line statements in JINJA


app.model = None
app.facolta = None
__user = ""
__password = ""


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/home', methods=['POST', 'GET'])
def homePage():
    """Home page deve presentare form per la scelta corso studi e
    anno accademico tra i corsi della facoltà di Scienze MM FF NN."""
    global __user
    global __password

    if request.method == 'POST':
        __user = request.form['username']
        __password = request.form['password']

    if app.model is None and app.facolta is None:
        app.model = Model(__user, __password)
        app.facolta = app.model.getFacolta("Scienze Matematiche Fisiche e Naturali")

    corsiStudi = app.model.getCorsiStudi(app.facolta['id'])
    aA = app.model.getAnniAccademici(app.facolta['id'])
    # print(type(app.facolta)) E' un dizionario modificato (psycopg2.extras.DictRow
    return render_template('homepage.html', facolta=app.facolta, corsiStudi=corsiStudi, aa=aA, prova="<b>prova</b>")


@app.route('/insegnamenti', methods=['POST', 'GET'])
def insegnamenti():
    '''Elenco degli insegnamenti di un corso di studi in un a.a.'''
    if request.method == 'POST':
        idCorsoStudi = request.form['idCorsoStudi']
        aA = request.form['aa']
    else:
        idCorsoStudi = request.args['idCorsoStudi']
        aA = request.args['aa']

    corsoStudi = app.model.getCorsoStudi(idCorsoStudi)
    insEroConDoc = app.model.getInsEroConDoc(idCorsoStudi, aA)
    return render_template('insegnamenti.html', facolta=app.facolta, corsoStudi=corsoStudi, idCorsoStudi=idCorsoStudi,
                           aa=aA, insErogati=insEroConDoc)


@app.route("/insegnamento", methods=['POST', 'GET'])
def insegnamento():
    """Dettagli di un insegnamento erogato"""

    idCorsoStudi = request.args['idCS']
    aA = request.args['aa']
    id = request.args['id']

    insegn = app.model.getInsegnDetails(id)[0]
    return render_template('insegnamento.html', ins=insegn, idCorsoStudi=idCorsoStudi, aa=aA)


if __name__ == '__main__':  # Questo if deve essere ultima istruzione.
    app.run(debug=True)  # Debug permette anche di ricaricare i file modificati senza rinizializzare il web server.
