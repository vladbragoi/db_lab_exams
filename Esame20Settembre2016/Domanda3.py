#Assumendo di avere una base di dati PostgreSQL che contenga le tabelle di #questo tema d’esame, scrivere un programma Python che, leggendo i dati da 
#console, inserisca una o più tuple nella tabella RAGGIUNGE facendo un 
#controllo preventivo che le eventuali dipendenze siano rispettate. Se una 
#dipendenza non è rispettata, il programma deve richiedere di reinserire il 
#dato associato alla dipendenza prima di procedere a inserire la tupla nella 
#tabella RAGGIUNGE. Il programma deve visualizzare l’esito di ogni singolo 
#inserimento. È richiesto che il programma suggerisca il tipo di dati da 
#inserire e che non ammetta possibilità di SQL Injection.


import psycopg2

autostrada=''
comune=''
numeroCaselli=''

with psycopg2.connect(host='localhost', database='esame20092016', user='postgres', password = '') as con:
	with con.cursor() as cur:
		inserisci = input("Vuoi inserire una tupla nella tabella raggiunge?.s=Si, n=No:")
		while inserisci != n:
			flag = True
			while flag:
				autostrada = input("inserisci autostrada:")
				cur.execute('select * from autostrada a where a.codice = %s', (autostrada,))
				lista = cur.fetchone()
				if not list:
					print('L''autostrada non esiste. Reinserisci.')
				else:
					flag = False
			flag = True
			while flag:
				comune = input("inserisci comune:")
				cur.execute('select * from comune c where c.codiceIstat = %s', (comune,))
				lista = cur.fetchone()
				if not list:
					print('Il comune non esiste. Reinserisci.')
				else:
					flag = False
			numeroCaselli = int(input('inserisci il numero di caselli:'))
			print("Esito inserimento tabella: ", cur.statusmessage)


