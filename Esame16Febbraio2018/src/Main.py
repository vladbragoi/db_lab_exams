import psycopg2.extras
from _functools import reduce

_user = "postgres"
_password = "postgres"
_con = psycopg2.connect(host="localhost", database="esami", user=_user, password=_password)
_con.set_session(isolation_level="SERIALIZABLE")


def get_cursor():
    return _con.cursor(cursor_factory=psycopg2.extras.DictCursor)


def create_tables():
    with get_cursor() as cur:
        cur.execute("""
            drop domain if exists tipoConvegno;
            create domain tipoConvegno as varchar
                check(value in ('seminario', 'simposio', 'conferenza'));
            
            drop table if exists convegno cascade; 
            create table convegno (
                nome varchar(30) primary key,
                dataInizio date not null,
                dataFine date check(dataFine >= dataInizio),
                numeroSessioni integer not null check (numeroSessioni > 0),
                tipo tipoConvegno not null,
                luogo varchar not null 
            );
            
            drop table if exists intervento cascade;
            create table intervento(
                id integer primary key,
                titolo varchar not null,
                relatore varchar not null,
                durata interval not null check(durata > '00:00'::interval)
            );
            
            drop table if exists sessione cascade;
            create table sessione (
                nome varchar,
                nomeConvegno varchar(30) references convegno(nome) on delete cascade,
                data date not null,
                orarioInizio time with time zone not null,
                orarioFine time with time zone not null check(orarioFine > orarioInizio),
                primary key(nome, nomeConvegno)
            );

            drop table if exists intervento_in_convegno cascade;
            create table intervento_in_convegno(
                nomeConvegno varchar(30) references convegno(nome) on delete cascade,
                idIntervento integer references intervento(id),
                nomeSessione varchar,
                orarioInizio time with time zone not null,
                foreign key(nomeSessione, nomeConvegno) references sessione(nome, nomeConvegno),
                primary key(nomeConvegno, idIntervento, nomeSessione)
            );

            insert into convegno(nome, dataInizio, dataFine, numeroSessioni, tipo, luogo)
                values	('Guittar Show', '2018-06-08', '2018-06-10', 3, 'conferenza', 'Padova'),
                        ('Polo Zanotto', '2018-06-19', '2018-06-21', 5, 'seminario', 'Verona'),
                        ('Tecnologie Industriali', '2017-09-16', '2018-09-16', 27, 'simposio', 'Marragnole');

            insert into intervento(id, titolo, relatore, durata)
                values  (1, 'Come cambiare le corde', 'Giovanni Boscaini', '01:10:19'::interval),
                        (2, 'Come cambiare i pannolini', 'Cristian Sandu', '00:05:00'::interval),
                        (3, 'Come montare una turbina', 'Leonardo Testolin', '01:30:00'::interval);
                        
            insert into sessione(nome, nomeConvegno, data, orarioInizio, orarioFine)
	            values('Sessione 404', 'Tecnologie Industriali', '2017-09-16',  '20:50:00+01', '23:50:00+01');

            insert into intervento_in_convegno(nomeConvegno,idIntervento, nomeSessione, orarioInizio)
	            values('Tecnologie Industriali', 3, 'Sessione 404', '20:50:00+01');	
        """)


def get_names(tabella):
    with get_cursor() as cur:
        cur.execute("SELECT nome FROM {}".format(tabella))
        return reduce(lambda x, y: x + y, list(cur))


def get_interventi():
    with get_cursor() as cur:
        cur.execute("SELECT id, titolo FROM INTERVENTO")
        return list(cur)


def check(tabella, nome):
    with get_cursor() as cur:
        cur.execute("SELECT 1 FROM {} WHERE nome ILIKE %s".format(tabella), (nome,))
        return not cur.fetchone()


def check_intervento(id):
    with get_cursor() as cur:
        cur.execute("SELECT 1 FROM INTERVENTO WHERE id = %s", (id,))
        return not cur.fetchone()


def check_orario(orario):
    with get_cursor() as cur:
        cur.execute(""" SELECT 1 FROM CONVEGNO C, SESSIONE S 
                        WHERE S.data BETWEEN C.dataInizio AND C.dataFine 
                        AND %s BETWEEN S.orarioInizio::time AND orarioFine::time""", (orario,))
        return not cur.fetchone()


def insert_intervento(convegno, id, sessione, orario):
    with get_cursor() as cur:
        cur.execute(""" INSERT INTO INTERVENTO_IN_CONVEGNO
                        VALUES (%s, %s, %s, %s)""", (convegno, id, sessione, orario))
        _con.commit()


def run():
    print("Convegni: \n", get_names("CONVEGNO"))
    nome_convegno = input("> ")
    while check("CONVEGNO", nome_convegno):
        nome_convegno = input("Errore, riprova [Q per uscire]: ")
        if nome_convegno.lower() == "q":
            exit(1)

    print("Sessioni: \n", get_names("SESSIONE"))
    nome_sessione = input("> ")
    while check("SESSIONE", nome_sessione):
        nome_sessione = input("Errore, riprova [Q per uscire]: ")
        if nome_sessione.lower() == "q":
            exit(1)

    print("Interventi: \n", get_interventi())
    id_intervento = input("id intervento: ")
    while check_intervento(int(id_intervento)):
        id_intervento = input("Errore, riprova [Q per uscire]: ")
        if id_intervento.lower() == "q":
            exit(1)

    orario_inizio = input("Orario dell'intervento: ")
    while check_orario(orario_inizio):
        orario_inizio = input("Errore, riprova [Q per uscire]: ")
        if orario_inizio.lower() == "q":
            exit(1)

    try:
        insert_intervento(nome_convegno, id_intervento, nome_sessione, orario_inizio)
        print("Tupla inserita!")
    except (Exception, psycopg2.Error):
        print("Errore inserimento. Riprovare")


if __name__ == "__main__":
    # create_tables()
    while(True):
        run()