--(a) Trovare per ogni autostrada che raggiunga almeno 10 comuni, il numero
-- totale di comuni che raggiunge e il numero totale di caselli, riportando 
--il codice dell’autostrada, la sua lunghezza e i conteggi richiesti.

create view conteggi as (

	select r.autostrada,r.comune, count(r.comune) as numComuni , sum(r.numeroCaselli) as numCaselli
	from raggiunge r
	group by(r.autostrada)

);


select c.autostrada, a.lunghezza, c.numComuni, c.numCaselli
from conteggi c join autostrada a on a.codice = c.autostrada
join comune co on co.codiceISTAT = c.comune
group by(c.autostrada)
having count(c.numComuni) >= 10;



--(b) Selezionare le autostrade che hanno un potenziale di utenti diretti 
--(=numero di abitanti che la possono usare dal loro comune) medio rispetto 
--al numero dei caselli dell’autostrada stessa superiore alla media degli 
--utenti per casello di tutte le autostrade. Si deve riportare il codice 
--dell’autostrada, il suo numero totale di utenti, la media di utenti per casello.


SELECT c.codice , co.numeroAbitanti , co.numeroAbitanti/c.numeroCaselli AS mediaPerCasello
FROM conteggi c join comune co on co.codiceISTAT = c.comune
WHERE co.numeroAbitanti/c.numeroCaselli >= ALL (
SELECT AVG(numeroAbitanti/numeroCaselli)
FROM utentiPerAutostrada 
);