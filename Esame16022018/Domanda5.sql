--L'indice utilizzato qui è ins_aa definito su tre attributi:
CREATE INDEX ins_aa ON inserogato(annoaccademico, crediti, modulo);
-- Supponendo che i dati non varino nel tempo (bisogna semplicemente guardare 
-- i costi di accesso e nient'altro, se i costi di accesso sono maggiori a 10
-- allora si creano altrimenti NON SI CREANO) e che le chiavi primarie hanno indice
-- create di default da Postgresql (quindi NON si creano MAI su queste );
-- Non vengono creati ulteriori indici perchè guardando i due nodi foglia 
-- contenenti seq scan(l'unico posto dove questi vengono creati):
-- 1) Siamo in una condizione di costo inferiore a 10 accessi nel primo(mi conviene
-- andare direttamente in tabella a recuperare le tuple ed evitare quindi 
-- il doppio passaggio attraverso l'indice), inoltre il nodo è di tipo Hash( NON si 
-- creano indici su tabella scansionate tramite funzioni di Hash che fa già il calcolo
-- degli indirizzi in memoria tramite le funzioni di hash)
-- 2) Il secondo nodo è un tipo Hash(NON si creano indici).