--Trovare i comuni che non sono raggiunti da autostrade gestite dal gestore X,
--riportando il codice, il nome e gli abitanti del comune.

select c.codiceIstat, c.nome, c.numeroAbitanti 
from raggiunge r join autostrada a on a.codice=r.autostrada
join comune c on c.codiceISTAT = r.comune
where a.codice not in(

	select a.codice
	from autostrada a
	where a.gestore = 'X'

);