import psycopg2

conn = None

# dados da connecÃ§Ã£o
host = 'localhost'
database = 'DropMusic'
user = 'postgres'
password = 'postgres'

def connect():
    # estabelece a conneccao com a bd
    global conn

    if conn == None:
        try:
            conn = psycopg2.connect(host=host,database=database, user=user, password=password)

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

def terminate():
    if conn is not None:
        conn.close()
        

def login(username, password):
    # verifica se existe um user com este username e password
    
    sql = '''SELECT username, pass, id_utilizador, privilegio 
             FROM utilizador
             WHERE username = %s and pass = %s'''

    
    if conn == None:
        connect()

    try:
        
        cur = conn.cursor()
        cur.execute(sql, (username, password, ))

        # nenhum user com esse username e password
        if cur.rowcount < 1:
            cur.close()
            return None
        
        # ir buscar a linha resultado do SQL
        data = cur.fetchone()
        user = {'id_utilizador': data[2], 'Status': data[3]}

        cur.close()
        return user

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None
    
def registo(username,password,nome,contacto,status):
    #inserir um novo utilizador na base de dados
    
    
    sql = '''insert into utilizador(username,pass,nome,contacto,privilegio) values(%s,%s,%s,%s,%s) returning id_utilizador;'''
    id_utilizador = None

    

    try:
        if conn == None:
            connect()
        cur = conn.cursor()
        cur.execute(sql,(username,password,nome,contacto,status, ))
        id_utilizador=cur.fetchone()[0]
        conn.commit()
        cur.close()
        return id_utilizador
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    
def insert_editora(nome):
    sql=''' insert into editora(editora) values(%s)'''

    if conn == None:
        connect()
    try:
        cur = conn.cursor()
        cur.execute(sql,(nome,))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    

def verificar_editora(nome):
    sql='''select editora from editora where editora=%s'''
    if conn == None:
        connect()
    try:
        cur = conn.cursor()
        cur.execute(sql,(nome,))
        if cur.rowcount < 1:
            cur.close()
            return None
        data = cur.fetchone()[0]
        editora = {'nome': data[0]}

        cur.close()
        return editora
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    

def insert_grupomusical(nome):
    sql=''' insert into grupo_musical(nome_grupomusical) values(%s) returning id_grupomusical'''
    if conn == None:
        connect()
    try:
        cur = conn.cursor()
        cur.execute(sql,(nome,))
        id_gm=cur.fetchone()[0]
        conn.commit()
        cur.close()
        return id_gm
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    


def verificar_grupomusical(nome):
    #Nao funciona
    sql='''select id_grupomusical,nome_grupomusical from grupo_musical where nome_grupomusical=%s'''
    if conn == None:
        connect()
    try:
        cur = conn.cursor()
        cur.execute(sql,(nome,))
        if cur.rowcount < 1:
            cur.close()
            return None
        id_gm = cur.fetchone()[0]
        
        cur.close()
        return id_gm
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    

def insert_musica(nome,nome_ed,id_gm,data,letra):
    sql=''' insert into musica(titulo,data_lancamento,letra,editora_editora,grupo_musical_id_grupomusical)
        values(%s,%s,%s,%s,%s) returning id_musica,grupo_musical_id_grupomusical'''
    
    if conn == None:
        connect()
    try:
        cur = conn.cursor()
        cur.execute(sql,(nome,data,letra,nome_ed,id_gm,))
        data= cur.fetchone()
        id_m={'id_m': data[0],'id_gm': data[1]}
        conn.commit()
        cur.close()
        return id_m
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    

def verificar_musica(nome):
    sql='''select id_musica,titulo,grupo_musical_id_grupomusical
        from musica where titulo=%s'''
    if conn == None:
        connect()
    try:
        cur = conn.cursor()
        cur.execute(sql,(nome,))
        if cur.rowcount < 1:
            cur.close()
            return None
        data=cur.fetchone()
        id_m = {'id_m': data[0] , 'id_gm': data[2]}
        cur.close()
        return id_m
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def insert_genero(nome):
    sql=''' insert into genero(tipo_genero) values(%s)'''
    
    if conn == None:
        connect()
    try:
        cur = conn.cursor()
        cur.execute(sql,(nome,))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def verificar_genero(nome):
    sql='''select tipo_genero from genero where tipo_genero=%s'''
    if conn == None:
        connect()
    try:
        cur = conn.cursor()
        cur.execute(sql,(nome,))
        if cur.rowcount < 1:
            cur.close()
            return None
        data = cur.fetchone()[0]
        genero= {'nome': data[0]}

        cur.close()
        return genero
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def insert_artista(nome,idade,nacio,tipo):
    sql=''' insert into artista(nome,idade,nacionalidade,tipo) values(%s,%s,%s,%s) returning id_musico,tipo'''
    
    if conn == None:
        connect()
    try:
        cur = conn.cursor()
        cur.execute(sql,(nome,idade,nacio,tipo,))
        data= cur.fetchone()
        tp={'id_musico':data[0],'tipo':data[1]}
        conn.commit()
        cur.close()
        return tp
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def insert_periodo(periodo,historia,id_gm):
    sql=''' insert into periodos(periodos,historia,grupo_musical_id_grupomusical) values(%s,%s,%s)'''
    
    if conn == None:
        connect()
    try:
        cur = conn.cursor()
        cur.execute(sql,(periodo,historia,id_gm,))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def insert_concerto(nome,data):
    sql=''' insert into concertos(nome_concerto,data_concerto) values(%s,%s)'''
    
    if conn == None:
        connect()
    try:
        cur = conn.cursor()
        cur.execute(sql,(nome,data,))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def verificar_concerto(nome):
    sql='''select nome_concerto from concertos where nome_concerto=%s'''
    if conn == None:
        connect()
    try:
        cur = conn.cursor()
        cur.execute(sql,(nome,))
        if cur.rowcount < 1:
            cur.close()
            return None
        data = cur.fetchone()[0]
        concerto= {'nome': data[0]}

        cur.close()
        return concerto
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def insert_gm_concerto(nome,id_gm):
    sql=''' insert into grupo_musical_concertos(grupo_musical_id_grupomusical,concertos_nome_concerto) values(%s,%s)'''
    
    if conn == None:
        connect()
    try:
        cur = conn.cursor()
        cur.execute(sql,(id_gm,nome,))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def insert_m_concerto(id_m,nome):
    sql=''' insert into musica_concertos(musica_id_musica,concertos_nome_concerto) values(%s,%s)'''
    
    if conn == None:
        connect()
    try:
        cur = conn.cursor()
        cur.execute(sql,(id_m,nome,))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def insert_art_gm(id_musico,id_gm):
    sql=''' insert into artista_grupo_musical(artista_id_musico,grupo_musical_id_grupomusical) values(%s,%s)'''
    
    if conn == None:
        connect()
    try:
        cur = conn.cursor()
        cur.execute(sql,(id_musico,id_gm,))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def insert_art_m(id_musico,id_m):
    sql=''' insert into artista_musica(artista_id_musico,musica_id_musica) values(%s,%s)'''
    
    if conn == None:
        connect()
    try:
        cur = conn.cursor()
        cur.execute(sql,(id_musico,id_m,))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def insert_album(nome_album,pontuacao,data_lanc,nome_editora,id_gm):
    sql=''' insert into album(pontuacao,nome_album,data_lancamento,editora_editora,grupo_musical_id_grupomusical) values(%s,%s,%s,%s,%s) returning id_album'''
    
    if conn == None:
        connect()
    try:
        cur = conn.cursor()
        cur.execute(sql,(pontuacao,nome_album,data_lanc,nome_editora,id_gm))
        id_album=cur.fetchone()
        conn.commit()
        cur.close()
        return id_album
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def insert_m_genero(id_m,genero):
    sql=''' insert into musica_genero(musica_id_musica,genero_tipo_genero) values(%s,%s)'''
    
    if conn == None:
        connect()
    try:
        cur = conn.cursor()
        cur.execute(sql,(id_m,genero,))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def insert_genero_al(genero,id_album):
    sql=''' insert into genero_album(genero_tipo_genero,album_id_album) values(%s,%s)'''
    
    if conn == None:
        connect()
    try:
        cur = conn.cursor()
        cur.execute(sql,(genero,id_album,))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def mostrar_letra(musica):
    sql='''Select id_musica, titulo, letra from musica where titulo = %s'''
    if conn == None:
        connect()

    try:
        cur = conn.cursor()
        cur.execute(sql, (musica, ))
        if cur.rowcount < 1:
            cur.close()
            return None
        data = cur.fetchone()
        musica_letra= {'id': data[0],'nome': data[1], 'letra':data[2]}
        cur.close()
        return musica_letra
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None
#ainda n usadas
def insert_critica(pont,just,id_album,id_m,id_uti):
    sql=''' insert into critica(pontuacao,justificacao,album_id_album,musica_id_musica,utilizador_id_utilizador) values(%s,%s,%s,%s,%s)'''
    
    if conn == None:
        connect()
    try:
        cur = conn.cursor()
        cur.execute(sql,(pont,just,id_album,id_m,id_uti,))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def insert_playlist(nome,pub,id_uti):
    sql=''' insert into playlist_(nome_playlist,publica,utilizador_id_utilizador) values(%s,%s,%s)'''
    
    if conn == None:
        connect()
    try:
        cur = conn.cursor()
        cur.execute(sql,(nome,pub,id_uti,))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def insert_pl_m(id_pl,id_m):
    sql=''' insert into playlist__musica(playlist_id_playlist_privada) values(%s,%s)'''
    
    if conn == None:
        connect()
    try:
        cur = conn.cursor()
        cur.execute(sql,(id_pl,id_m,))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def mostrar_compositores(id_musica):
    sql='''Select nome from artista where id_musica=%s'''
    if conn == None:
        connect()

    try:
        cur = conn.cursor()
        cur.execute(sql, (id_musica, ))
        if cur.rowcount < 1:
            cur.close()
            return None
        data = cur.fetchone()
        nome_comp= {'nome': data[0]}
        cur.close()
        return nome_comp
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None
    
