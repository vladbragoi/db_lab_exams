"""DataMapper verso PostgreSQL.
Questa classe permette di essere usata in diversi modi.
La connessione è un oggetto condiviso da tutte le istanze della classe.
La connessione viene chiusa quando non c'è nessuna istanza della classe attiva.
@author: posenato"""
from datetime import datetime
import logging
import psycopg2.extras
import getpass


class DM_PG():
	"""Data mapper verso PostgreSQL. Per semplicità, i parametri di connessione sono attributi di classe:
	dovrebbero essere scritti in un file esterno e caricati durante __init__."""

	__server = "dbserver.scienze.univr.it"
	__db = "did2014"
	__db4Log = 'id878cue'
	__user = 'id878cue'
	__pw = ""
	__dbCon = None  # La connessione è condivisa!
	__db4LogCon = None  # La connessione è condivisa!
	__nIstanze = 0

	@classmethod
	def __open(cls):
		if cls.__dbCon is None:
			try:
				cls.__dbCon = psycopg2.connect(host=cls.__server, database=cls.__db, user=cls.__user, password=cls.__pw)
				cls.__dbCon.set_session(readonly=True, autocommit=True)  # Connessione di lettura condivisa
				logging.info("Connection to database " + cls.__db + " created.")
			except psycopg2.OperationalError as err:
				logging.error("Error connecting to PostgreSQL DBMS at %s.\nDetails: %s.", cls.__server, err)
				cls.__dbCon = cls.__db4LogCon = None
				exit()
			else:  # No exceptions was raised.
				try:
					cls.__db4LogCon = psycopg2.connect(host=cls.__server, database=cls.__db4Log, user=cls.__user, password=cls.__pw)
					cls.__db4LogCon.set_session(autocommit=True)  # Connessione di scrittura condivisa
					logging.info("Connection to database " + cls.__db4Log + " created.")
				except psycopg2.OperationalError as err:
					logging.error("Error connecting to PostgreSQL DBMS at %s.\nDetails: %s.", cls.__server, err)
					cls.__dbCon = cls.__db4LogCon = None
					exit()
				return "New connection opened."
		return "Connection already opened."

	@classmethod
	def __close(cls):
		if cls.__nIstanze == 0 and cls.__dbCon is not None:
			cls.__dbCon.close()
			cls.__db4LogCon.close()
			logging.info("Connection closed.")
			cls.__dbCon = cls.__db4LogCon = None

	@classmethod
	def __cursor(cls):
		"""Ritorna un cursore che restituisce dict invece di tuple per ciascuna riga di una select."""
		return cls.__dbCon.cursor(cursor_factory=psycopg2.extras.DictCursor)

	@classmethod
	def __cursor4log(cls):
		"""Ritorna un cursore per scrivere nel database cls.__db4Log."""
		return cls.__db4LogCon.cursor()

	def __init__(self, user, password):
		DM_PG.__user = user
		DM_PG.__pw = password
		DM_PG.__open()  # IGNORE:protected-access
		DM_PG.__nIstanze += 1  # IGNORE:no-member Instance

	def close(self):
		"""Chiude in modo esplicito la connessione, se non ci sono altre istanze attive"""
		self.__del__()

	def __del__(self):
		DM_PG.__nIstanze -= 1  # IGNORE:no-member Instance
		DM_PG.__close()  # IGNORE:protected-access

	def __enter__(self):  # per istruzione 'with'
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):  # per istruzione 'with'
		pass

	def getFacolta(self, name):
		"""Ritorna il dict {id, nome, url, dataCreazione} della facoltà di nome "name" se esite, None altrimenti."""
		with DM_PG.__cursor() as cur:
			cur.execute("SELECT id, nome, url, datacreazione FROM Facolta WHERE nome ILIKE %s", (name,))
			facolta = cur.fetchone()
			return facolta

	def getCorsoStudiFacolta(self, idF):
		"""Ritorna una list di dict {id, nome,codice, durataAnni} di tutti i corsi di studi associati alla facoltà con id 'idF'"""
		with DM_PG.__cursor() as cur:
			cur.execute("""select cs.id, cs.nome, cs.codice, cs.durataanni as "durataAnni"
						from corsostudi cs join corsoinfacolta csf on cs.id =csf.id_corsostudi
						where csf.id_facolta=%s order by cs.nome""", (int(idF),))
			return list(cur)

	def getAnniAccademiciFacolta(self, idF):
		"""Ritorna una list di stringhe rappresentanti gli anni accademici di tutti i corsi di studi associati alla facoltà con id 'idF'"""
		with DM_PG.__cursor() as cur:
			cur.execute("""select distinct ie.annoaccademico as aa
						from inserogato ie join  corsostudi cs on ie.id_corsostudi = cs.id
							join corsoinfacolta csf on cs.id =csf.id_corsostudi
						where csf.id_facolta=%s order by ie.annoaccademico desc""", (int(idF),))
			lista = list()
			for tupla in cur:
				lista.append(tupla[0])
			return lista

	def getCorsoStudi(self, idCS):
		"""Ritorna dict {idCS, nome,codice, durataAnni, annoaccademico, stato} del corso di studi 'idCS'"""
		with DM_PG.__cursor() as cur:
			cur.execute("""select cs.id, cs.nome, cs.codice, cs.durataanni as "durataAnni"
					, scs.annoaccademico as "annoAccademicoUltimoStato", st.valore as "ultimoStato"
				from corsostudi cs join statodics scs on cs.id =scs.id0_corsostudi
					join statocs st on scs.id1_statocs = st.id
				where cs.id=%s order by annoaccademico desc""", (int(idCS),))
			return cur.fetchone()

	def getInsEroConDoc(self, idCS, annoA):
		"""Ritorna una list di dict {id, nome,discr,hamoduli, modulo,nomeModulo, discriminanteModulo, haunita, nomeUnita, crediti, docente}
		di tutti gli insegnamenti erogati del corso di studi 'idCS' nell'anno accademico 'annoA'"""
		with DM_PG.__cursor() as cur:
			cur.execute("""select distinct ie.id,i.nomeins as nome, d.nome as discr, ie.hamoduli, abs(ie.modulo) as modulo,
							ie.nomemodulo as "nomeModulo", ie.discriminantemodulo as "discriminanteModulo",
							ie.haunita, ie.nomeunita as "nomeUnita", ie.crediti, p.nome || ' ' || p.cognome as docente
							from inserogato ie join insegn i on ie.id_insegn=i.id
								join corsostudi cs on ie.id_corsostudi=cs.id
								left join discriminante d on ie.id_discriminante = d.id
								left join docenza doc on doc.id_inserogato = ie.id
								join persona p on doc.id_persona =p.id
							where cs.id = %s and ie.annoaccademico= %s
							order by i.nomeins, modulo""", (int(idCS), annoA))
			return list(cur)

	def getInsegnDetails(self, idInsegn):
		with DM_PG.__cursor() as cur:
			cur.execute(""" select i.nomeins, i.codiceins, cs.nome as corsoStudi, d.nome as "discriminante", 
									ie.crediti, ie.programma, f.nome as "facoltà", ie.annierogazione, 
									p.nome || ' ' || p.cognome as docente
							from insegn i join inserogato ie on ie.id_insegn = i.id 
								join discriminante d on ie.id_discriminante = d.id 
								join corsoStudi cs on ie.id_corsostudi = cs.id 
								join corsoInFacolta cif on cif.id_corsoStudi = cs.id 
								join facolta f on cif.id_facolta = f.id 
								left join docenza doc on doc.id_inserogato = ie.id
								join persona p on doc.id_persona =p.id
							where ie.id = %s;""", (int(idInsegn),))
			return list(cur)


	def log(self, idModel: str, instant: datetime, methodName: str):
		"""Scrive il log sulla tabella InsegnamentiLog che deve essere presente nel database cls.__database4Log.
		CREATE TABLE INSEGNAMENTILOG (
			id SERIAL PRIMARY KEY,
			idModeApp VARCHAR NOT NULL,
			instant TIMESTAMP NOT NULL,
			methodName VARCHAR NOT NULL)"""
		if idModel is None or methodName is None or instant is None:
			return
		with DM_PG.__cursor4log() as cur:
			cur.execute("INSERT INTO InsegnamentiLog (idModeApp, instant, methodName) VALUES (%s,%s,%s)",
				(idModel, instant, methodName))
			if cur.rowcount != 1:
				logging.error("Log has not been written. Details: " + idModel + ", " + str(instant) + "," + methodName)
				return False
			return True


if __name__ == '__main__':
	# Just for test as program
	with DM_PG("id878cue", getpass.getpass()) as db:
		#print(str(db.getFacolta("Scienze Matematiche Fisiche e Naturali")))
		#print(db.getCorsoStudiFacolta(1))
		#print(db.getAnniAccademiciFacolta(1))
		#print(db.getCorsoStudi(216))
		#for d in db.getInsEroConDoc(419, '2011/2012'):
		#	print(d)
		print(db.getInsegnDetails("81176"))
