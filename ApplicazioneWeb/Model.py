"""Semplice Model applicazione 'Insegnamenti'.
Questo Model mantiene anche un log delle chiamate ai metodi.
La separazione con il database è forzata.
@author: posenato"""

from datetime import date, datetime
from DM_PG import DM_PG

class Model(object):
    """Realizza il modello dei dati da pubblicare."""

    def __init__(self, user, password):
        self.user = user
        self.password = password
        self.id = "Model_" + date.today().isoformat()
        self.dataMapper = DM_PG(user, password)  # DataMapper verso PostgreSQL

    def getFacolta(self, name):
        """Ritorna struct della facoltà con nome 'name'"""
        fac = self.dataMapper.getFacolta(name)
        self.dataMapper.log(self.id, datetime.today(), 'getFacolta')
        return fac

    def getCorsiStudi(self, idF):
        """Ritorna list di {id, nome,codice, durataAnni} dei corsi di studio della facolta 'idFS'"""
        cs = self.dataMapper.getCorsoStudiFacolta(int(idF))
        self.dataMapper.log(self.id, datetime.today(), 'getCorsiStudi')
        return cs

    def getAnniAccademici(self, idF):
        """Ritorna list di stringhe con gli anni accademici presenti nei corsi di studio della facoltà 'idFS'"""
        aa = self.dataMapper.getAnniAccademiciFacolta(int(idF))
        self.dataMapper.log(self.id, datetime.today(), 'getAnniAccademici')
        return aa

    def getInsEroConDoc(self, corsoStudi, annoA):
        """Ritorna lista ins. erogati nel 'corsoStudi' nell'anno accademico 'annoA'. Ogni elemento della lista è {id, nome,discr,hamoduli, modulo,nomeModulo, discriminanteModulo, haunita, nomeUnita, crediti, docente}"""
        listaIns = self.dataMapper.getInsEroConDoc(int(corsoStudi), annoA)
        if not listaIns:  # una lista vuota è sempre false!
            return listaIns
        # listaIns può avere più righe per uno stesso insegnamento se ci sono più docenti.
        # Tali righe si devono unire unendo i docenti.
        listaInsFinale = []
        rigaPrecedente = listaIns[0]
        for riga in listaIns:
            if riga['id'] == rigaPrecedente['id'] and riga != rigaPrecedente:
                riga['docente'] += "\n" + rigaPrecedente['docente']
            else:
                listaInsFinale.append(rigaPrecedente)
            rigaPrecedente = riga
        listaInsFinale.append(rigaPrecedente)
        self.dataMapper.log(self.id, datetime.today(), 'getInsEroConDoc')
        return listaInsFinale

    def getCorsoStudi(self, idCS):
        """Ritorna {idCS, nome,codice, durataAnni, annoaccademico, stato} del corso di studi 'idCS' dove stato è lo stato di attivazione."""
        cs = self.dataMapper.getCorsoStudi(int(idCS))
        self.dataMapper.log(self.id, datetime.today(), 'getCorsoStudi')
        return cs

    def getInsegnDetails(self, idInsegn):
        """Ritorna una lista con i dettagli sull'insegnamento idInsegn.
         Ogni elemento della lista è {nomeins, codiceins, corsostudi, discriminante, crediti, programma, facoltà, annierogazione, docente}"""
        lista = self.dataMapper.getInsegnDetails(int(idInsegn))
        self.dataMapper.log(self.id, datetime.today(), 'getInsegnDetails')
        return lista

    def __del__(self):
        self.dataMapper.close()  # Chiudere sempre il DataMapper
