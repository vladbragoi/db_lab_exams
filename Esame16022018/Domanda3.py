import psycopg2 

with psycopg2.connect(host = 'localhost' database='esame1602018', user = 'postgres', password='') as con:
	con.isolation_level = 'SERIALIZABLE'
	with con.cursor() as cur:
		nomeConvegno=''
		idIntervento=''
		nomeSessione=''
		orarioInizio=''
		choice = input('Vuoi inserire una tupla? s=Si, n=No:')
		while choice != 'n':
			flag = True
			while flag:
				nomeConvegno = input('Inserisci il nome di un convegno (varchar):')
				cur.execute("""select * from convegno c where c.nome= %s""", (nomeConvegno,))
				lista = list(cur)
				if lista != None:
					flag = False
				else:
					print('Valore inserito errato.')
			flag = True
			while flag:
				idIntervento = int(input('Inserisci un idIntervento (intero):'))
				cur.execute("""select * from intervento i where i.id= %s""", (idIntervento,))
				lista = list(cur)
				if lista != None:
					flag = False
				else:
					print('Valore inserito errato.')
			flag = True
			while flag:
				nomeSessione = input('Inserisci un nomeSessione (varchar):')
				cur.execute("""select * from sessione s where s.nome= %s""", (nomeSessione,))
				lista = list(cur)
				if lista != None:
					flag = False
				else:
					print('Valore inserito errato.')
			flag = True
			while flag:
				orarioInizio = input('Inserisci un datetime:')
				#orarioInizio = datetime.datetime.strptime()
				cur.execute(""" SELECT 1 FROM CONVEGNO C, SESSIONE S 
                        WHERE S.data BETWEEN C.dataInizio AND C.dataFine 
                        AND %s BETWEEN S.orarioInizio::time AND orarioFine::time""", (orarioInizio,))
				lista = list(cur)
				if lista != None:
					flag = False
				else:
					print('Valore inserito errato.')
			cur.execute(""" INSERT INTO INTERVENTO_IN_CONVEGNO
                        VALUES (%s, %s, %s, %s)""", (nomeConvegno, idIntervento, nomeSessione, orarioInizio))
			print(cur.statusmessage)

con.close()