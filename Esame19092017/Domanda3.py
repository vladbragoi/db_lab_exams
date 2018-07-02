@app.route('/prenota', methods=['post','get'])
def prenota():
    cf = ""
    iataC = ""
    numerovolo = 0
    orarioVolo = ""
    isbusiness = True
    listares = list()

    if request.method = 'post':
        cf = request.form['cf']
        iataC = request.form['iata']
        numerovolo = request.form['nv']
        orarioVolo = request.form['ov']
        isbusiness = request.form['bus']
    else:
        cf = request.args['cf']
        iataC = request.args['iata']
        numerovolo = request.args['nv']
        orarioVolo = request.args['ov']
        isbusiness = request.args['bus']

    with psycopg2.connect(databse='X') as con:
        with con.cursor() as cur:
            cur.execute(
                """
                select (v.postiBusiness-v.postiBusinessComprati) as b, (v.postiEconomy-v.postiEconomyComprati) as e
                from volo v
                where v.iataCompagnia = %s
                        and v.numero = %s
                        and v.orariopartenza = %s
                """,(iataC,numerovolo,orariopartenza)
            )
            listares = cur.fetchAll()

            if not listares:
                return render_template('nessunVoloOPostiEsauriti.html')
            if isbusiness and listares[0] > 0:
                cur.execute(""" update volo set postibusinesscomprati = postibusinesscomprati + 1 where iataCompagnia= %s and numero = %s and orarioPartenza = %s """,(iataC, numerovolo, orarioVolo) )
                cur.execute("""Insert into prenotazione values(%s,%s,%s,%s,%s)""" , (iataC, numerovolo, orarioVolo, cf, isbusiness) )
                return render_template('prenotazioneEffettuata.html')
            elif not isbusiness and listares[1] > 0:
                cur.execute(""" update volo set postieconomycomprati = postieconomycomprati + 1 where iataCompagnia= %s and numero = %s and orarioPartenza = %s """,(iataC, numerovolo, orarioVolo) )
                cur.execute("""Insert into prenotazione values(%s,%s,%s,%s,%s)""" , (iataC, numerovolo, orarioVolo, cf, isbusiness) )
                return render_template('prenotazioneEffettuata.html')
            else:
                render_template('nessunVoloOPostiEsauriti.html')
    conn.close()