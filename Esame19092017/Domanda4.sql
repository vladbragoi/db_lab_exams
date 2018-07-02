--Scrivere in PostgreSQL l’interrogazione che determina, per ciascun volo 
--dall’aeroporto di MPX all’aeroporto di LGW nel giorno 31 ottobre 2017 
--(nel fuso orario dell’Europa Centrale), il numero di clienti maschi
-- già prenotati. Il risultato deve mostrare la chiave del volo, i codici 
--dei due aeroporti e il conteggio richiesto.

select v.iataCompagnia, v.numero, v.orarioPartenza, v.partenza, v.destinazione, count(*)
from volo v join prenotazione p on v.iataCompagnia = p.iataCompagnia and v.numero=p.numeroVolo and v.orarioPartenza=p.orarioPartenza
join cliente c on c.codiceFiscale=p.codiceFiscale
where v.partenza = 'MPX' and v.destinazione='LGW' and  v.orarioPartenza>='2017-10-31 00:00:00 +01' and v.orarioPartenza<='2017-11-01 00:00:00 +01' and c.sesso='M'
group by (v.iataCompagnia, v.numero, v.orarioPartenza);
