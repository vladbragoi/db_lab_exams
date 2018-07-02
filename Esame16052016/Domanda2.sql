--Scrivere il codice PostgreSQL per trovare i clienti che non hanno 
--mai noleggiato auto della marca ‘X’, riportando il cognome, 
--il nome e la provenienza del cliente.

select c.cognome, c.nome, c.paeseProvenienza
from cliente c join noleggio n on c.nPatente = n.cliente
 join auto a on a.targa = n.targa
where c.nPatente not in (

	select c.nPatente
	from cliente c join noleggio n on c.nPatente = n.cliente
 join auto a on a.targa = n.targa
 	where a.marca ilike 'Ford'

);

