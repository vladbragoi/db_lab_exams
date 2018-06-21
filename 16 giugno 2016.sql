-- Domanda 1
DROP TABLE IF EXISTS AUTO;
CREATE TABLE AUTO(
    targa CHAR(7) PRIMARY KEY CHECK (targa SIMILAR TO '[A-Z]{2}[0-9]{3}[A-Z]{2}'),
    marca VARCHAR(20) NOT NULL,
    modello VARCHAR(20) NOT NULL,
    posti INTEGER NOT NULL CHECK (posti > 0 AND posti < 10),
    cilindrata INTEGER NOT NULL CHECK(cilindrata > 0)
);

DROP TABLE IF EXISTS CLIENTE;
CREATE TABLE CLIENTE(
    nPatente VARCHAR(10) PRIMARY KEY,
    cognome VARCHAR(30) NOT NULL,
    nome VARCHAR(30) NOT NULL,
    paeseProvenienza VARCHAR(30) NOT NULL,
    nInfrazioni INTEGER NOT NULL DEFAULT 0 CHECK(nInfrazioni >= 0)
);

DROP TABLE IF EXISTS NOLEGGIO;
CREATE TABLE NOLEGGIO (
    targa CHAR(7),
    cliente VARCHAR(10),
    inizio TIMESTAMP,
    fine TIMESTAMP CHECK (fine > inizio),
    PRIMARY KEY (targa, cliente, inizio),
    FOREIGN KEY (targa) REFERENCES AUTO,
    FOREIGN KEY (cliente) REFERENCES CLIENTE
);

-- Domanda 2
SELECT C.cognome, C.nome, C.paeseProvenienza
FROM CLIENTE C
WHERE C.nPatente NOT IN (
    SELECT C.nPatente
    FROM CLIENTE CL
        JOIN NOLEGGIO N ON N.cliente = C.nPatente
        JOIN AUTO A ON N.targa = A.targa
    WHERE A.marca = 'X'
);

