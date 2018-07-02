--Trovare per ogni utente che abbia fatto prenotazioni con almeno due 
--compagnie distinte, il numero di voli già effettuati (finiti) all’istante 
--corrente presso ciascuna compagnia e la loro durata totale, sempre per 
--ciascuna compagnia. Il risultato deve riportare il codice fiscale 
--dell’utente, il codice ICAO della compagnia aerea e i conteggi richiesti.

create view conteggi as (

	select p.codiceFiscale, v.icaoCompagnia, count(p.numeroVolo) as numVoli , sum(v.durata) as durate
	from volo v join prenotazione p on v.iataCompagnia = p.iataCompagnia and v.numero=p.numeroVolo and v.orarioPartenza=p.orarioPartenza
	where v.orarioPartenza + v.durata >= current_timestamp 
	group by(p.codiceFiscale, v.icaoCompagnia)

	);

select c.codiceFiscale, c.icaoCompagnia, c.numVoli, c.durate
from conteggi c
where c.codiceFiscale in (

	select c1.codiceFiscale
	from conteggi c1
	where c1.icaoCompagnia <> c.icaoCompagnia

)
group by(c.codiceFiscale, c.icaoCompagnia, c.numVoli ,c.durate);



--Trovare per ogni compagnia (specificata solo dal suo ICAO), l’utente
-- (gli utenti) con il maggior numero di voli e l’utente (gli utenti) che ha 
 --(hanno) totalizzato il tempo di volo complessivo maggiore, riportando nel
 -- risultato: ICAO della compagnia, il codice fiscale dell’utente e i 
 --conteggi richiesti (se gli utenti per ciascuna compagnia coincidono, 
 --si deve stampare solo una riga). Si può non tenere conto se i voli sono 
 --già stati effettuati o no all’instante corrente.


 select c.icaoCompagnia, c.codiceFiscale, c.numVoli , c.durate
 from conteggi c
 where c.numVoli >= ALL( select max(c1.numVoli) from conteggi c1)
 or c.durate >= ALL(select max(c1.durate) from conteggi c1)
 group by (c.icaoCompagnia, c.codiceFiscale, c.numVoli , c.durate);