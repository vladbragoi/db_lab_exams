import model
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def main():
    citta = model.get_citta()
    return render_template("index.html", citta=citta)


@app.route("/telefonateCittaData")
def telefonateCittaData():
    citta = request.args['citta']
    data = request.args['data']

    clienti = model.Clienti(citta, data)

    if len(clienti) == 0:
        return render_template("erroreParametri.html")

    for cliente in clienti:
        cliente['cognome'] = cliente['cognome'].upper()

    return render_template("view.html", clienti=clienti)


if __name__ == "__main__":
    model.create_tables()
    app.run(debug=True)