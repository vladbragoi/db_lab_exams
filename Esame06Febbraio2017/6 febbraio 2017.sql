-- Domanda 1
CREATE DOMAIN LIVELLO AS VARCHAR(15) 
    CHECK(VALUE IN ('principiante', 'intermedio', 'avanzato'));

CREATE DOMAIN GM AS VARCHAR(10)
    CHECK(VALUE IN ('petto', 'schiena', 'spalle', 'braccia', 'gambe'));

CREATE DOMAIN GIORNOSETTIMANA AS CHAR(3)
    CHECK(VALUE IN ('lun', 'mar', 'mer', 'gio', 'ven', 'sab', 'dom'));

CREATE TABLE ESERCIZIO(
    nome VARCHAR(30) PRIMARY KEY,
    livello LIVELLO NOT NULL,
    gruppoMuscolare GM NOT NULL
);

CREATE TABLE PROGRAMMA(
    nome VARCHAR(30) PRIMARY KEY,
    livello LIVELLO NOT NULL
);

CREATE TABLE ESERCIZIO_IN_PROGRAMMA(
    nomeProgramma VARCHAR(30) REFERENCES PROGRAMMA(nome),
    giorno GIORNOSETTIMANA,
    nomeEsercizio VARCHAR(30) REFERENCES ESERCIZIO(nome),
    ordine INTEGER CHECK (ordine >= 0) NOT NULL,
    serie INTEGER CHECK(serie >= 0) NOT NULL,
    ripetizioni INTEGER CHECK(ripetizioni >= 0) NOT NULL,
    TUT INTEGER NOT NULL REFERENCES TUT(id),
    riposo INTEGER NOT NULL CHECK(riposo >= 0),
    PRIMARY KEY(nomeProgramma, giorno, nomeEsercizio)
)

CREATE TABLE TUT(
    id INTEGER PRIMARY KEY,
    valore1 INTEGER NOT NULL CHECK(valore1 >= 0),
    valore2 INTEGER NOT NULL CHECK(valore2 >= 0),
    valore3 INTEGER NOT NULL CHECK(valore3 >= 0),
    valore4 INTEGER NOT NULL CHECK(valore4 >= 0)
)

-- Domanda 2
/* Dato il nome ’X’ di un programma di allenamento, scrivere una query che visualizzi tutti gli esercizi da fare
(con tutti i dati necessari per l’esecuzione) ordinati per i giorni di allenamento e ordine di esecuzione. Si deve
anche visualizzare il gruppo muscolare dell’esercizio. */

SELECT EP.nomeEsercizio, EP.serie, EP.ripetizioni, EP.TUT, EP.riposo, E.gruppoMuscolare
FROM ESERCIZIO E
    JOIN ESERCIZIO_IN_PROGRAMMA EP ON EP.nomeEsercizio = E.nome
WHERE EP.nomeProgramma = 'X'
ORDER BY EP.giorno, EP.ordine;

-- Domanda 4 a
/* Trovare per ogni programma di allenamento distribuito su almeno 3 giorni il numero totale di esercizi da
svolgere e il tempo totale in minuti per ciascun giorno di allenamento. Il risultato deve visualizzare nome
programma di allenamento, giorno e i conteggi richiesti per l’allenamento del giorno considerato.
Suggerimento: Ogni ripetizione di esercizio richiede un tempo pari alla somma dei valori del TUT. Per esempio,
se il TUT è (4,1,4,1), il tempo totale di una ripetizione è 10 s. Ogni serie richiede un tempo pari al tempo TUT
moltiplicato per il numero di ripetizioni più il tempo di riposo a fine serie. Il tempo di una serie moltiplicato per
il numero di serie è il tempo totale (in s) per fare l’esercizio. */

SELECT EP.nomeProgramma, EP.giorno, COUNT(EP.nomeEsercizio), 
    (SUM(((T.valore1 + T.valore2 + T.valore3 + T.valore4) * EP.ripetizioni + EP.riposo) * EP.serie))
FROM ESERCIZIO_IN_PROGRAMMA EP
    JOIN TUT T ON EP.TUT = T.id
GROUP BY EP.nomeProgramma, EP.giorno
HAVING COUNT(DISTINCT EP.giorno) >= 3;

-- Domanda 4 b
/* Trovare tutti i programmi di allenamento (visualizzando nome e livello) ciascuno dei quali contiene esercizi
di livello ’principiante’ per il gruppo muscolare ’gambe’, ha una durata di almeno 45 minuti per ciascun
giorno e non contiene esercizi di qualsiasi livello per il gruppo muscolare ’petto’. */

SELECT DISTINCT EP.nomeProgramma, P.livello
FROM ESERCIZIO_IN_PROGRAMMA EP
    JOIN PROGRAMMA P ON EP.nomeProgramma = P.nome
    JOIN TUT T ON EP.TUT = T.id
WHERE 
    EP.nomeEsercizio IN (
        SELECT E1.nome
        FROM ESERCIZIO E1
        WHERE E1.livello = 'principiante'
            AND E1.gruppoMuscolare = 'gambe'
    )
    AND EP.nomeEsercizio NOT IN(
        SELECT E2.nome 
        FROM ESERCIZIO E2
        WHERE E1.gruppoMuscolare = 'petto'
    )
GROUP BY EP.nomeProgramma, P.livello, EP.giorno
HAVING SUM(((T.valore1 + T.valore2 + T.valore3 + T.valore4) * EP.ripetizioni + EP.riposo) * EP.serie) >= (45 * 60);

-- Domanda 5 a
/* Considerando le query della domanda 2, si consideri il seguente risultato del comando ANALYZE su una
query che risponde alla domanda 2:
Sort ( cost =4.08..4.10 ROWS =9 width =49)
    Sort KEY : e . giorno , e . ordine
    -> Hash JOIN ( cost =2.45..3.93 ROWS =9 width =49)
        Hash Cond : (( e . nomeesercizio ) :: TEXT = ( es . nome ) :: TEXT )
        -> Hash JOIN ( cost =1.36..2.72 ROWS =9 width =43)
            Hash Cond : (( e . tut ) :: TEXT = ( t . id ) :: TEXT )
            -> Seq Scan ON esercizio_in_programma e( cost =0.00..1.24 ROWS =9 width =32)
                Filter : (( nomeprogramma ) :: TEXT = ' ABC ' :: TEXT )
            -> Hash ( cost =1.16..1.16 ROWS =16 width =19)
                -> Seq Scan ON tut t ( cost =0.00..1.16 ROWS =16 width =19)
        -> Hash ( cost =1.04..1.04 ROWS =4 width =14)
            -> Seq Scan ON esercizio es ( cost =0.00..1.04 ROWS =4 width =14)
(a) Indicare quanti e quali indici sono stati usati per risolvere la query giustificando la risposta. */

NESSUNO

-- Domanda 5 b
/* (b) Supponendo che i dati non varino nel tempo, in base al piano di esecuzione conviene creare degli indici?
Se sì, quali? */

Sì: CREATE INDEX ep_nome_programma_index ON ESERCIZIO_IN_PROGRAMMA(nomeProgramma);
    CREATE INDEX ep_nome_esercizio ON ESERCIZIO_IN_PROGRAMMAnomeEsercizio);