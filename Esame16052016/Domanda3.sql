--Scrivere il codice PostgreSQL, definendo anche eventuali viste, 
--per rispondere alle seguenti due interrogazioni nel modo più efficace:
--(a) Trovare per ogni marca d’auto 
-- che ha avuto almeno un noleggio: 
--il numero complessivo di auto di quella marca,
-- il numero di noleggi 
--in cui è stata utilizzata un’auto di quella marca e 
--il numero complessivo di ore di noleggio per le auto di quella marca,
-- riportando la marca e i tre conteggi richiesti.


create view conteggi as(
	
	select a.marca, COUNT(distinct a.targa) as numAuto, COUNT(*) as numNoleggi, 
			SUM(EXTRACT(epoch FROM ((n.fine - n.inizio)))/3600) as numore 
	from noleggio n join auto a on n.targa=a.targa
	where n.fine is not null
	group by (a.marca)
	
	);

	select * from conteggi;

--(b) Trovare la marca con il massimo numero di ore di noleggio visualizzando 
--la marca e il numero di ore di noleggio.
--Suggerimento: la funzione EXTRACT(epoch FROM <INTERVAL>) restituisce 
--l’intervallo in secondi.
	
	select cc.marca, cc.numore
	from conteggi cc
	where numore = (select max(cc.numore) from conteggi cc)
	group by(cc.marca, cc.numore);

