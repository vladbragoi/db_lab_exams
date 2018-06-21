"""
@author: 
Si vuole salvare in un file una tabella delle spese definita come
table spese {
    data DATE,
    voce VARCHAR,
    importo Decimal
}
In questo modulo si rappresenta la tabella come un oggetto di una
classe e si usa JSON per salvare.
Inoltre gli importi sono rappresentati come Decimal.
"""
# IMPORT
from datetime import datetime, date
import decimal
import json
import re

#################################################################
# CLASSI o funzioni di servizio
pattern = re.compile("^\d{2,2}/\d{2,2}/\d{4,4}$")

def creaDict(data, voce, importo):
        """
        Ritorna un dict formato con gli argomenti.
        Formato: {'data': <data>, 'voce': <voce>, 'importo: <importo>}
        Fa il check sul formato data e su importo che deve essere
        Decimal.
        """
        if not isinstance(data, date):
            print("Data non è nel formato dd/mm/aaaa o non in formato Date")
            exit()
        if not isinstance(importo, decimal.Decimal) and not \
            isinstance(importo, str):
            print("Importo deve essere un Decimal o una stringa che"
                  " rappresenta un importo.")
            exit()

        return {'data':data, 'voce':voce, 'importo':decimal.Decimal(importo)}

class Spese:
    """L'attributo 'tabella' rappresenta le spese organizzate
        come dict (primaryKey, riga).
        La primaryKey è data dalla coppia(data, voce).
        L'attributo 'ultimaModifica' rappresenta il timestamp
        dell'ultima modifica.
    """
    @staticmethod
    def makeKey(data, voce):
        return str(data) + "_%_" + voce

    def __init__(self, inputTab={}, istante=datetime.now()):
        self.tabella = dict(inputTab)
        self.ultimaModifica = istante

    def add(self, data, voce, importo):
        self.tabella[Spese.makeKey(data, voce)] = creaDict(data, voce, importo)
        self.ultimaModifica = datetime.now()
        return importo

    def remove(self, data, voce):
        del self.tabella[Spese.makeKey(data, voce)]
        self.ultimaModifica = datetime.now()

    def get(self, data, voce):
        return self.tabella[self.makeKey(data, voce)]

    def items(self):
        return self.tabella.items()

################################################################################
# Creo la tabella e aggiungo dati
tab = Spese()
tab.add(datetime.strptime("24/02/2016", "%d/%m/%Y").date(), "Stipendio", "0.1")
tab.add(datetime.strptime("24/02/2016", "%d/%m/%Y").date(), 'Stipendio "Bis"', "0.1")
tab.add(datetime.strptime("24/02/2016", "%d/%m/%Y").date(), 'Stipendio "Tris"', "0.1")
tab.add(datetime.strptime("27/02/2016", "%d/%m/%Y").date(), 'Affitto', "-0.3")

# Stampo la tabella da memoria
print("=" * 50)
print("| {:10s} | {:<20} | {:>10s} |".format("Data", "Voce", "Importo"))
print("-" * 50)

for riga in tab.tabella.values():
    print("| {:10s} | {:<20} | {:>10.2f} |".format(riga['data'].isoformat(), riga['voce'], riga['importo']))
print("=" * 50)

# Calcolo il totale degli importi
tot = decimal.Decimal(0)
for riga in tab.tabella.values():
    tot += riga['importo']
print("La somma è {:.20f}".format(tot))

# Salvataggio in un file
class MyEncoder(json.JSONEncoder):
    """Codifica gli oggetti di tipo Decimal, Date o Spese."""
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        if isinstance(o, date):
            return o.isoformat()
        if isinstance(o, Spese):
            return {"tabella":o.tabella, "ultimaModifica": o.ultimaModifica}
        return json.JSONEncoder.default(self, o)

# Salvo la tabella in un file
nomeFile = 'database.json'
with open(nomeFile, mode='w', encoding='utf-8') as file:
    json.dump(tab, file, cls=MyEncoder, indent=4)


def myDecoder(jsonObj):
    """Decodifica oggetti di tipo Spesa."""
    if 'tabella' in jsonObj:
        tab = jsonObj['tabella']
        istante = datetime.strptime(jsonObj['ultimaModifica'], "%Y-%m-%dT%H:%M:%S.%f")
        return Spese(tab, istante)
    else:
        return jsonObj

# Leggo dal file la tabella e la pongo in una nuova variabile
with open(nomeFile, mode='r', encoding='utf-8') as file:
    tab1 = json.load(file, object_hook=myDecoder, parse_float=decimal.Decimal)

# Calcolo il totale sulla nuova tabella
tot1 = decimal.Decimal(0)
for riga in tab1.tabella.values():
    tot1 += riga['importo']

if tot == tot1:
    print("I due totali sono uguali!")
if tot == 0:
    print("Eureka!")
else:
    print("Ops... il totale non è corretto!")
