-- Domanda 1
CREATE TABLE INGREDIENTE(
    id INTEGER PRIMARY KEY,
    nome VARCHAR(30) NOT NULL,
    calorie INTEGER CHECK(calorie > 0)
    grassi INTEGER NOT NULL,
    proteine INTEGER NOT NULL,
    carboidrati INTEGER NOT NULL,
    CHECK((grassi + proteine + carboidrati) <= 100)
);

CREATE DOMAIN REGIONI AS VARCHAR(30) 
    CHECK(VALUE IN('Valle d''aosta', 'Lombardia', 'Trentino-alto-adige', 'Friuli-venezia-giulia', 'Veneto', 'Piemonte', 
        'Liguria', 'Emilia-romagna', 'Toscana', 'Marche', 'Umbria', 'Lazio', 'Abbruzzo', 'Molise', 'Puglia', 'Campania',
        'Basilicata', 'Calabria', 'Sicilia', 'Sardegna'));

CREATE TABLE RICETTA(
    id INTEGER PRIMARY KEY,
    nome VARCHAR(30) NOT NULL,
    regione REGIONI NOT NULL,
    porzioni INTEGER NOT NULL,
    tempoPreparazione INTERVAL NOT NULL,
);

CREATE TABLE COMPOSIZIONE(
    ricetta INTEGER REFERENCES RICETTA(id),
    ingrediente INTEGER REFERENCES INGREDIENTE(id),
    quantita INTEGER CHECK(quantita > 0),
    PRIMARY KEY(ricetta, ingrediente)
);

-- Domanda 2
SELECT R.nome, R.tempoPreparazione 
FROM RICETTA R
    JOIN COMPOSIZIONE C ON C.ricetta = R.id
    JOIN INGREDIENTE I ON C.ingrediente = I.id
WHERE R.regione = 'Veneto'
    AND (I.carboidrati/100)::REAL >= 0.4;

-- Domanda 3 a
SELECT R.nome, SUM(C.quantita * I.proteine), SUM(C.quantita * I.grassi)
FROM RICETTA R 
    JOIN COMPOSIZIONE C ON C.ricetta = R.id
    JOIN INGREDIENTE I ON C.ingrediente = I.id
GROUP BY R.nome;

-- Domanda 3 b
SELECT R.nome, SUM(C.quantita * I.grassi)
FROM RICETTA R 
    JOIN COMPOSIZIONE C ON C.ricetta = R.id
    JOIN INGREDIENTE I ON C.ingrediente = I.id
WHERE SUM(C.quantita * I.grassi / R.porzione) IN (
    SELECT MAX(C1.quantita * I1.grassi / R1.porzione)
    FROM RICETTA R1
        JOIN COMPOSIZIONE C1 ON C1.ricetta = R1.id
        JOIN INGREDIENTE I1 ON C1.ingrediente = I1.id
    WHERE R.nome = R1.nome
)
GROUP BY R.nome;