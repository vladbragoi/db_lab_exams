select s.nomeConvegno,  extract(day from s.data) as giorno, count(*) as numInterventi, sum(i.durata) as durataInterventi 
from sessione s join intervento_in_convegno ic 
on s.nome = ic.nomeSessione and s.nomeConvegno = ic.nomeConvegno
join intervento i on i.id = ic.idIntervento
group by(s.nomeConvegno, giorno);




select s.nomeConvegno,  extract(day from s.data) as giorno, count(*) as numInterventi, sum(i.durata) as durataInterventi 
from sessione s join intervento_in_convegno ic 
on s.nome = ic.nomeSessione and s.nomeConvegno = ic.nomeConvegno
join intervento i on i.id = ic.idIntervento
group by(s.nomeConvegno, giorno)
having count(distinct(extract(day from s.data))) >= 3; 