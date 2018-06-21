'''
Modified on Apr 28, 2018

In questo programma si assume che lo studente NON sappia usare le funzioni di Flask per leggere i dati del request.
Questo programma  FUNZIONA solo con un giocatore alla volta!
@author: posenato
'''

from _random import Random
from flask import Flask

app = Flask("Gioco")
# Alcune variabili dell'applicazione per rappresentare lo stato e le costanti del gioco.
app.rnd = Random()
app.rnd.seed()
app.sequence = [0, 0, 0]
app.seqMaxIndex = 2
app.index = 0
app.moves = 0
app.maxAllowedMoves = 10

# Le seguenti variabili (in realtà costanti stringa) sono per scrivere pezzi di codice HTML in modo semplice
# Sono variabili di MODULO!
head = """<!DOCTYPE html>
<html>
<head>
	<title>Piccolo gioco</title>
	<style type="text/css">
		form, input {
			padding: 2px;
			width: auto;
			text-align: center;
		}
		input {
			font-size: x-large;
			padding: 5px;
		}
	</style>
</head>
<body>
"""

form = """
<form action="/pushed0" method="get">
	<input type="submit" value="0">
</form>
<form action="/pushed1" method="get">
	<input type="submit" value="1">
</form>
"""

tail = """
<form style="text-align: right" action="/" method="get">
	<input type="submit" value="Mi sono rotto, ricomincia!">
</form>
"""

def makeRandomSequence():
    '''Genera una sequenza casuale di 3 bit e la memorizza nell'attributo app.sequence.'''
    tmp = bin(Random().getrandbits(3))[2:]
    while len(tmp) < 3:
        tmp = "0" + tmp
    print(tmp)
    app.sequence = list(tmp)


def availableMoves():
    '''Ritorna il numero di mosse ancora possibili'''
    return app.maxAllowedMoves - app.moves


@app.route('/')
def homePage():
    '''Inizializza il gioco e ritorna il codice HTML per la home page.'''
    makeRandomSequence()
    app.index = 0
    app.moves = 0
    return head + """
	<h1>Piccolo gioco di fortuna</h1>
	<p>Il giocatore deve indovinare una sequenza casuale di Vero o False di lunghezza 3.</p>
	<p>Ogni volta che il giocatore indovina un mossa, il gioco va avanti. Ogni volta che il giocatore sbaglia una mossa, il gioco ricomincia.</p>
	<p>Il giocatore vince se indovina una sequenza entro 10 mosse.</p>
	""" + form + tail

@app.route('/pushed0')
def falseButton():
    return manageButton(False)


@app.route('/pushed1')
def trueButton():
    return manageButton(True)


def manageButton(rightValue):
    '''Realizza la logica del gioco. Ritorna il codice HTML della pagina di risposta in base allo stato del gioco e alla mossa fatta e passata in input'''
    app.moves += 1
    if availableMoves() <= 0:
        answer = "<p>Hai terminato le mosse possibili.</p><h3>Hai perso!</h3>"
    elif app.index >= len(app.sequence):
        app.moves = 0
        answer = "<h4> Ricomincia il gioco! </h4>" + form
    elif rightValue == False and app.sequence[app.index] == '0'\
            or rightValue == True and app.sequence[app.index] == '1':
        app.index += 1
        if app.index >= len(app.sequence):
            answer = "<h3> Hai vinto </h3>" + form
            app.moves = 0
        else:
            answer = "<p> Forse hai indovinato </p>" + form
    else:
        answer = "<p> Hai palesemente sbagliato!!! </p>" + form
    return head + answer + tail

if __name__ == '__main__':
    app.run(debug=True)