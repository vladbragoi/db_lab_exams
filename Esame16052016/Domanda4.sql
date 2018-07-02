--Scrivere il codice PostgreSQL che crei uno o più indici che possono migliorare
--le prestazioni dell’interrogazione della seconda domanda giustificando la scelta. 
--Attenzione a non creare indici già presenti (per ogni indice proposto già presente 
--la valutazione è penalizzata)!


select cc.marca, cc.numore
	from conteggi cc
	where numore = (select max(cc.numore) from conteggi cc)
	group by(cc.marca, cc.numore);


-- non creo alcun indice in quanto la querry è basata su una view
-- l'unica cosa che posso fare è velocizzare la creazione della view ma questo non è richiesto

