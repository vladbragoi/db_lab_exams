-- Domanda 1
-- Vincolo di integrità mancante CLIENTE.citta -> CITTA
CREATE TABLE CITTA (
    codice INTEGER,
    nome VARCHAR(30) NOT NULL,
    PRIMARY KEY (codice)
);

CREATE TABLE CLIENTE(
    codice INTEGER,
    nome VARCHAR(30) NOT NULL,
    cognome VARCHAR(30) NOT NULL,
    nTelefono VARCHAR(14) NOT NULL,
    indirizzo VARCHAR(50) NOT NULL,
    citta INTEGER,
    PRIMARY KEY (codice),
    FOREIGN KEY (citta) REFERENCES CITTA(codice)
);

CREATE DOMAIN TIPOCONTRATTO AS VARCHAR(15) 
    CHECK (VALUE IN ('privato', 'business', 'corporate')
);

CREATE TABLE CONTRATTO(
    contratto INTEGER,
    cliente INTEGER NOT NULL,
    tipo TIPOCONTRATTO NOT NULL,
    dataInizio DATE NOT NULL,
    dataFine DATE,
    PRIMARY KEY (contratto),
    FOREIGN KEY (cliente) REFERENCES CLIENTE(codice),
    CHECK (dataInizio < dataFine)
);

CREATE TABLE TELEFONATA(
    contratto INTEGER,
    nTelChiamato VARCHAR(14),
    istanteInizio TIMESTAMP,
    durata INTERVAL NOT NULL,
    PRIMARY KEY (contratto, nTelChiamato, istanteInizio),
    FOREIGN KEY (contratto) REFERENCES CONTRATTO(contratto)
);

-- Domanda 2
SELECT CL.cognome, CL.nome, CL.indirizzo
FROM CLIENTE CL
    JOIN CITTA CI ON CL.citta = CI.codice
    JOIN CONTRATTO CO ON CO.cliente = CL.codice
    JOIN TELEFONATA T ON T.contratto = CO.contratto
WHERE CI.nome = 'Padova'
    AND T.istanteInizio < CURRENT_DATE
    AND T.istanteInizio >= CURRENT_DATE - 1
    AND (
        T.istanteInizio < (CURRENT_DATE - 1 + TIME '10:00')
        OR T.istanteInizio > (CURRENT_DATE - 1 + TIME '17:00')
    )
;

INSERT INTO CITTA VALUES(1, 'Padova');
INSERT INTO CLIENTE VALUES(1, 'Filippo', 'Contro', '+39 3497094222', 'via Dossi, 66 Oppeano(VR)', 1);
INSERT INTO CONTRATTO VALUES(1, 1, 'privato', '1/01/2018', '1/01/2019');
INSERT INTO TELEFONATA VALUES(1, '+39 3925093287', CURRENT_DATE - 1 + TIME '15:08', '00:03:58');

-- Domanda 4
SELECT CO.dataInizio, CO.contratto, COUNT(T.contratto), SUM(T.durata)
FROM CONTRATTO CO
    JOIN TELEFONATA T ON T.contratto = CO.contratto
WHERE EXTRACT(MONTH FROM CO.dataInizio) = 1 
    AND EXTRACT(YEAR FROM CO.dataInizio) = 2007
    AND EXTRACT(MONTH FROM T.istanteInizio) = 5
    AND EXTRACT(YEAR FROM T.istanteInizio) = 2007
GROUP BY CO.dataInizio, CO.contratto;

DROP VIEW IF EXISTS NUMTELEFONATE;
CREATE TEMP VIEW NUMTELEFONATE(contratto, mese, num_telefonate) AS (
    SELECT T.contratto, EXTRACT(MONTH FROM T.istanteInizio), COUNT(*)
    FROM TELEFONATA T 
    WHERE EXTRACT(YEAR FROM T.istanteInizio) = 2016
    GROUP BY T.contratto, EXTRACT(MONTH FROM T.istanteInizio)
);
SELECT NT.contratto, NT.mese, MAX(NT.num_telefonate)
FROM NUMTELEFONATE NT
GROUP BY NT.contratto, NT.mese;

