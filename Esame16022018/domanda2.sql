select ic.nomeSessione, i.titolo, i.relatore, ic.orarioInizio
from intervento_in_convegno ic join intervento i on i.id = ic.idIntervento
where ic.nomeConvegno = 'Tecnologie Industriali'
order by (ic.orarioInizio);