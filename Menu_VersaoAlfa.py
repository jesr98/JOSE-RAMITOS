import os
import api
#from pygame import mixer


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def validate_option(op, max_op, min_op):
    # valida se a opçao um valor inteiro, e se se encontra entre min e max, inclusive
    try:
        op = int(op)
        if op >= min_op and op <= max_op:
            return op
        else:
            clear()
            print("\nValor incorreto, introduza um numero entre %d e %d" % (min_op, max_op))
            return False
    except:
        pass


def input_numero(mensagem):
    while True:
        try:
            userInput = int(input(mensagem))
        except ValueError:
            clear()
            print("\nIsso não é um numero inteiro, introduza um numero")
            continue
        else:
            return userInput
            break


def drop_music():
    opcao = input_numero("\n♬ DROP MUSIC ♬\n\n 1. Login \n 2. Registo \n 3. Sair \n\n Opcao: ")
    if not(validate_option(opcao, 3, 1)):
        drop_music()
    else:

        if opcao == 1:
            clear()
            login()
        elif opcao == 2:
            clear()
            registo()
        elif 3:
            print("🎧 Ate a proxima 🎧")
            api.terminate()
            exit()


def login():
    login.username = input("\nUsername: ")
    password = input("Password: ")
    user = api.login(login.username, password)
    if user is not None:
        print("Login com sucesso!")
        login.status = user['Status']
        login.id = user['id_utilizador']

    if user is None:
        print("Username ou Password estao incorretos, tente outra vez")
        login()
    clear()
    menu_user()

def registo():
    username = input("\nUsername: ")
    password = input("Password: ")
    nome = input("Nome: ")
    contacto = input("Contacto: ")

    status = input_numero("\n1. Editor \n2. Nao Editor \n Status: ")
    if not(validate_option(status, 2, 1)):
        registo()

    api.registo(username, password, nome, contacto, status)

    print("Bem-vindo, " + username + " à DropMusic \n")
    drop_music()


def menu_user():
    menu = input_numero("\n♫ Main Menu ♫ \n\n 1. Pesquisar \n 2. Criticas \n 3. Playlist \n 4. Editar \n 5. Sair \n\n Opcao: ")
    if not(validate_option(menu, 5, 1)):
        menu_user()

    if menu == 1:
        clear()
        menu_pesquisar()
    elif menu == 2:
        clear()
        menu_criticas()
    elif menu == 3:
        clear()
        menu_playlists()
    elif menu == 4:
        if login.status == 1:
            clear()
            menu_editar()
        elif login.status == 2:
            print(login.username + "apenas Editores podem editar \n")
            menu_user(login.status)
    elif menu == 5:
        print("\n🎧 Ate a proxima 🎧")
        api.terminate()
        exit()


def menu_editar():
    editar = input_numero("\nMenu Editar \n\n 1. Editar Musica \n 2. Editar Album \n 3. Editar Grupo Muscal \n 4. Menu Inserir \n 5. Menu Eliminar \n 6. Main Menu \n\n Opcao: ")
    if not(validate_option(editar, 6, 1)):
        menu_editar()

    if editar == 1:
        nome_musica = input("Introduzir Nome da Musica: ")
        #sql
    elif editar == 2:
        nome_album = input("Introduzir Nome do Album: ")
        #sql
    elif editar == 3:
        nome_grupo_musical = input("Introduzir Nome do Grupo Musical: ")
        # sql
    elif editar == 4:
        clear()
        menu_editar_inserir()
    elif editar == 5:
        clear()
        menu_editar_eliminar()
    elif editar == 6:
        clear()
        menu_user()


def menu_editar_inserir():
    inserir = input_numero("\nMenu Inserir \n\n 1. Inserir Musica \n 2. Inserir Album \n 3. Inserir Grupo Muscal \n 4. Inserir Artista \n 5. Inserir Genero \n 6. Inserir Concerto \n 7. Inserir Periodos \n 8. Main Menu \n\n Opcao: ")
    if not (validate_option(inserir, 8, 1)):
        menu_editar()

    if inserir == 1:        #inserir musica
        nome_musica = input("Nome da musica:")
        data = input("Data de lançamento(ex DD-MM-AAAA):")
        letra = input("Letra da musica:")
        nome_editora = input("Nome da editora:")
        nome_grupomusical = input("Nome da grupo musical:")
        ver = api.verificar_editora(nome_editora)
        if ver is None:
            api.insert_editora(nome_editora)

        id_gm = api.verificar_grupomusical(nome_grupomusical)

        if id_gm is None:
            id_gm = api.insert_grupomusical(nome_grupomusical)

        verm = api.verificar_musica(nome_musica)
        if verm is None:
            verm = api.insert_musica(nome_musica, nome_editora, id_gm, data, letra)  # preciso de completar
        if verm['id_m'] is None:
            if not verm['id_gm'] == id_gm:
                api.insert_musica(nome_musica, nome_editora, id_gm, data, letra)
            elif verm['id_gm'] == id_gm:
                print("Musica já exite na base de dados")
                # sair
        genero = input("Genero da musica:")
        aux = api.verificar_genero(genero)
        if aux is None:
            api.insert_genero(genero)
        api.insert_m_genero(verm['id_m'], genero)

        menu_editar_inserir()

    elif inserir == 2:  #inserir album
        nome_album = input("Nome do album:")
        pontuacao = input("Pontuaçao do album:")
        data_lanc = input("Data de lancamento do album(ex DD-MM-AAAA):")
        nome_editora = input("Nome da editora:")
        ver = api.verificar_editora(nome_editora)
        if ver is None:
            api.insert_editora(nome_editora)
        nome_gm = input("Nome do Grupo Musical:")
        ver = api.verificar_grupomusical(nome_gm)
        if ver is None:
            id_gm = api.insert_grupomusical(nome_gm)
        if ver is not None:
            id_gm = ver['id_gm']
        id_album = api.insert_album(nome_album, pontuacao, data_lanc, nome_editora, id_gm)
        genero = input("Gennero do album:")
        aux = api.verificar_genero(genero)
        if aux is None:
            api.insert_genero(genero)
        api.insert_genero_al(genero, id_album)
        menu_editar_inserir()

    elif inserir == 3:          #inserir grupo_musical
        nome_grupomusical = input("Nome da grupo musical: ")
        periodo = input("Data de criaçao do grupo musical(ex.: DD-MM-AAAA): ")
        historia = input("Historia da criaçao da banda: ")
        ver = api.verificar_grupomusical(nome_grupomusical)
        if ver is None:
            id_gm = api.insert_grupomusical(nome_grupomusical)
        if ver is not None:
            print("Grupo musical já existe")
            # voltar ao menu
        api.insert_periodo(periodo, historia, id_gm)
        menu_editar_inserir()

    elif inserir == 4:          #inserir Artista
        artista = input("Nome do Artista: ")
        idade = input("Idade do Artista: ")
        nacio = input("Nacionalidade do Artista: ")
        tipo = input("\n1. Musico \n 2. Compositor \n Opcçao: ")
        tp = api.insert_artista(artista, idade, nacio, tipo)
        if tp['tipo'] == 1:
            op = 1
            while op == 1:
                nome_gm = input("Nome do grupo musical  a que pertence: ")
                id_gm = api.verificar_grupomusical(nome_gm)
                if id_gm is None:
                    id_gm = api.insert_grupomusical(nome_gm)
                api.insert_art_gm(tp['id_musico'], id_gm)
                op=input("Deseja adicionar o artista a mais algum grupo musical?\n 1. Sim \n 2. Nao \n\n Opcao: ")
        if tp['tipo'] == 2:
            op = 1
            while op == 1:
                nome_m = input("Nome da musica  que foram criadas pelo compositor: ")
                id_m = api.verificar_musica(nome_m)
                if id_m == None:
                    data = input("Data de lançamento(ex DD-MM-AAAA): ")
                    letra = input("Letra da musica: ")
                    nome_editora=input("Nome da editora: ")
                    ver = api.verificar_editora(nome_editora)
                    if ver is None:
                        api.insert_editora(nome_editora)
                    id_m = insert_musica(nome_m, nome_editora, id_gm, data, letra)
                api.insert_art_m(tp['id_musico'], id_m)
                op=input("Deseja adicionar o artista a mais algum grupo musical?\n 1. Sim \n 2. Nao \n\n Opcao: ")
        menu_editar_inserir()

    elif inserir == 5:  # inserir genero
        genero = input("Nome do genero: ")
        api.insert_genero(genero)
        menu_editar_inserir()
    elif inserir == 6:              #inserir concerto
        nome = input("Nome do concerto: ")
        data = input("Data do concerto: ")
        aux = api.verificar_concerto(nome)
        if aux is None:
            api.insert_concerto(nome, data)
        nome_gm = input("Nome do grupo musical que atuou no concerto: ")
        id_gm = api.verificar_grupomusical(nome_gm)
        if id_gm is None:
            id_gm = api.insert_grupomusical(nome_gm)
        api.insert_gm_concerto(nome, id_gm)
        nome_m = input("Nome da musica que foi tocada no concerto: ")
        id_m = api.verificar_musica(nome_m)
        if id_m is None:
            data = input("Data de lançamento(ex.:DD-MM-AAAA): ")
            letra = input("Letra da musica: ")
            nome_editora = input("Nome da editora: ")
            ver = api.verificar_editora(nome_editora)
            if ver is None:
                api.insert_editora(nome_editora)
            id_m = api.insert_musica(nome_m, nome_editora, id_gm, data, letra)

        api.insert_m_concerto(id_m['id_m'], nome)
        menu_editar_inserir()

    elif inserir == 7:
        print("falta inserir periodos")
        menu_editar_inserir()
    elif inserir == 8:
        api.terminate()
        clear()
        menu_user()


def menu_editar_eliminar():
    eliminar = input_numero("\nMenu Eliminar \n\n 1. Eliminar Musica \n 2. Eliminar Album \n 3. Eliminar Grupo Muscal \n 4. Eliminar Artista \n 5. Eliminar Genero \n 6. Eliminar Concerto \n 7. Eliminar Periodos \n 8. Main Menu \n\n Opcao: ")
    if not (validate_option(eliminar, 8, 1)):
        menu_editar()
    if eliminar == 1:
        print ("eliminar musica")

    elif eliminar == 2:
        print("eliminar album")

    elif eliminar == 3:
        print("eliminar grupo_musical")

    elif eliminar == 4:
        print("eliminar Artista")

    elif eliminar == 5:
        print("eliminar genero")

    elif eliminar == 6:
        print("eliminar concerto")

    elif eliminar == 7:
        print("falta inserir periodos")
    elif eliminar == 8:
        api.terminate()
        clear()
        menu_user()


def menu_pesquisar():

    menu_pesquisa = input_numero("\nMenu Pesquisar \n\n 1. Pesquisa Musica \n 2. Pesquisa Album \n 3. Pesquisa Grupo Musical \n 4. Pesquisa Genero \n 5. Playlist \n 6. Main Menu \n\n Opcao: ")
    if not(validate_option(menu_pesquisa, 6, 1)):
        menu_pesquisar()

    if menu_pesquisa == 1:
        nome_musica = input("Introduzir Nome da Musica: ")
        if api.verificar_musica(nome_musica) is None:

            if login.status == 1:
                opcao = input_numero("\nMusica nao existe. \n 1. Introduzir a musica %s \n 2. Nao Introduzir \n\n Opcao: "%(nome_musica))
                while not (validate_option(opcao, 2, 1)):
                    opcao = input_numero("\nMusica nao existe. \n 1. Introduzir a musica %s \n 2. Nao Introduzir \n\n Opcao: " % (nome_musica))
                if opcao == 1:
                    nome_musica = input("Nome da musica: ")
                    data = input("Data de lançamento(ex.: DD-MM-AAAA): ")
                    letra = input("Letra da musica: ")
                    nome_editora = input("Nome da editora: ")
                    nome_grupomusical = input("Nome da grupo musical: ")
                    ver = api.verificar_editora(nome_editora)
                    if ver is None:
                        api.insert_editora(nome_editora)

                    id_gm = api.verificar_grupomusical(nome_grupomusical)

                    if id_gm is None:
                        id_gm = api.insert_grupomusical(nome_grupomusical)

                    verm = api.verificar_musica(nome_musica)
                    if verm is None:
                        verm = api.insert_musica(nome_musica, nome_editora, id_gm, data, letra)  # preciso de completar
                    if verm['id_m'] is None:
                        if not verm['id_gm'] == id_gm:
                            api.insert_musica(nome_musica, nome_editora, id_gm, data, letra)
                        elif verm['id_gm'] == id_gm:
                            print("Musica já exite na base de dados")
                            # sair
                    genero = input("Genero da musica: ")
                    aux = api.verificar_genero(genero)
                    if aux is None:
                        api.insert_genero(genero)
                    api.insert_m_genero(verm['id_m'], genero)
                elif opcao == 2:
                    clear()
                    menu_pesquisar()

            menu_musica(nome_musica)
        elif login.status == 2:
            print("Musica inserida nao existe")
            menu_pesquisar()


    elif menu_pesquisa == 2:
        nome_album = input("Introduzir Nome do Album: ")
        clear()
        menu_album(nome_album)
    elif menu_pesquisa == 3:
        nome_grupo_musical = input("Introduzir Nome do Grupo Musical: ")
        clear()
        menu_grupo_musical(nome_grupo_musical)
    elif menu_pesquisa == 4:
        nome_genero = input("Introduzir Nome do Genero Musical: ")

    elif menu_pesquisa == 5:
        clear()
        menu_playlists()
    elif menu_pesquisa == 6:
        clear()
        menu_user()


def menu_musica(musica):
    menu_musica = input_numero("\nMenu Musica \n 1. Ouvir \n 2. Letra \n 3. Compositores \n 4.Criticas \n 5. Concertos \n 6. Adicionar a Playlist \n 7. Compartir \n 8. Main Menu \n\n Opcao: ")
    if not(validate_option(menu_musica, 8, 1)):
        menu_musica()

    if menu_musica == 1:
        clear()
        menu_ouvir(musica)
    elif menu_musica == 2:
        letra = api.mostrar_letra(musica)  # sql para buscar a letra
        if letra is not None:
            print("Letra da musica : " + letra['nome'] + " : " + letra['letra'])
    elif menu_musica == 3:
        id_musica = api.mostrar_letra(musica)  # aproveitei a funçao da letra para ir buscar o id
        if id_musica is not None:
            comp = api.mostrar_compositores(id_musica['id'])  # sql buscar compositores (acho que se relaciona com o id da musica nao tenho a certeza)
            if comp is not None:
                print("Compositores da musica" + id_musica['nome'] + " : " + comp['nome'])
    elif menu_musica == 4:
        clear()
        menu_criticas(musica)
    elif menu_musica == 5:
        clear()
        menu_concertos(musica)
    elif menu_musica == 6:
        clear()
        menu_adicionar_playlist(musica)
    elif menu_musica == 7:
        clear()
        menu_compartir(musica)
    elif menu_musica == 8:
        clear()
        menu_user()


def menu_album():
    menu_album = input_numero("\nMenu Album \n\n 1. Musicas \n 2. Grupo Musical \n 3. Criticas \n 4. Main Menu \n\n Opcao: ")
    if not (validate_option(menu_album, 4, 1)):
        menu_grupo_musical()

    if menu_album == 1:
        clear()
        menu_musica() #nome do album
    elif menu_album == 2:
        clear()
        menu_grupo_musical()
    elif menu_album == 3:
        clear()
        menu_criticas()
    elif menu_album == 4:
        clear()
        menu_user()


def menu_grupo_musical():
    menu_grupo_musical = input_numero("\nMenu Grupo Musical \n\n 1. Artistas \n 2. Musicas \n 3. Albuns \n 4.Periodos \n 5. Concertos \n 6. Main Menu \n\n Opcao: ")
    if not(validate_option(menu_grupo_musical, 6, 1)):
        menu_grupo_musical()

    if menu_grupo_musical == 1:
        print("#sql artistas")
    elif menu_grupo_musical == 2:
        print("#sql musicas        ? menu musicas")
    elif menu_grupo_musical == 3:
        print("#sql albuns         ? menu_albuns")
    elif menu_grupo_musical == 4:
        clear()
        menu_editar_periodos()
    elif menu_grupo_musical == 5:
        clear()
        menu_concertos(menu_grupo_musical.menu_grupo_musical)  #sql?
    elif menu_grupo_musical == 6:
        clear()
        menu_user()


def menu_grupo_album():
    menu_grupo_album = input_numero("\nMenu Grupo Musical \n 1. Musicas \n 2. Grupo Musical \n 3. Criticas \n 4. Main Menu \n\n Opcao: ")
    if not(validate_option(menu_grupo_album, 4, 1)):
        menu_grupo_album()

    if menu_grupo_album == 1:
        print("#sql musicas album")
    elif menu_grupo_album == 2:
        print("#sql grupo musical")
    elif menu_grupo_album == 3:
        print("#sql criticas")
    elif menu_grupo_album == 4:
        clear()
        menu_user()


def menu_minhas_criticas():
    menu_minhas_criticas = input_numero("\nMenu Minhas Criticas \n 1. Editar Critica \n 2. Apagar Critica \n 3. Main Menu \n\n Opcao: ")
    if not(validate_option(menu_minhas_criticas, 3, 1)):
        menu_grupo_musical()

    if menu_minhas_criticas == 1:
        nome_critica=input("Inserir Nome da Critica a Editar: ")

        print("#sql editar critica?")
    elif menu_minhas_criticas == 2:
        print("#sql apagar critica")
    elif menu_minhas_criticas == 3:
        clear()
        menu_user()


def menu_criticas():
    menu_criticas = input_numero("\nMenu Criticas \n\n 1. Escrever Critica \n 2. Procurar por Critica \n 3. Minhas por Critica \n 4. Main Menu \n\n Opcao: ")
    if not(validate_option(menu_criticas, 4, 1)):
        menu_criticas()

    if menu_criticas == 1:
        clear()
        menu_escrever_critica()
        nome_musica=input("Insira o nome da musica: ")
        #sql
    elif menu_criticas == 2:
        nome_critica=input("Insira nome da critica: ")
        #sql apresenta tabela das criticas com nome
    elif menu_criticas == 3:
        clear()
        menu_minhas_criticas()
    elif menu_criticas == 4:
        clear()
        menu_user()


def menu_escrever_critica():
    critica = input("Critica: ")
    pontuacao = input_numero("Pontuacao de 0 a 10: ")
    while pontuacao <= 0 or pontuacao > 10:
        pontuacao = input("Insira uma pontuacao entre 0 e 10: ")
    print("A sua critica foi registada com uma pontuacao de " + pontuacao + " ♪")
    #guardar na tabela criticas no sql
    clear()
    menu_user()


def menu_compartir (musica):
    usuario = input("Inserir nome de usurario: ")
    #sql para compartir com usuario
    #menu_compartir = int(input("Menu Compartir \n 1. Introduzir Nome do Usuario \n 2.Menu \n Opcao: "))


def menu_playlists():
    menu_playlist = input_numero("\nMenu Playlists \n\n 1. Minhas Playlists \n 2. Procurar por Playlists Publicas \n 3. Criar Playlists \n 4. Main Menu \n\n Opcao: ")
    if not(validate_option(menu_playlist, 4, 1)):
        menu_playlist()

    if menu_playlist == 1:
        clear()
        menu_minhas_playlists()
    elif menu_playlist == 2:
        clear()
        menu_playlists_publicas()
    elif menu_playlist == 3:
        clear()
        menu_criar_playlist()
    elif menu_playlist == 4:
        clear()
        menu_user()


def menu_minhas_playlists():
    menu_minhas_playlists = input_numero("\nMenu Minhas Playlists \n 1. Introduzir Nome da Minhas Playlists \n 2. Voltar \n 3. Main Menu \n\n Opcao: ")
    if not(validate_option(menu_minhas_playlists, 3, 1)):
        menu_minhas_playlists()

    if menu_minhas_playlists == 1:
        nome_minha_playlist = input("Introduzir Nome da Minha Playlist: ")
        menu_minhas_playlists_musicas(nome_minha_playlist)
    elif menu_minhas_playlists == 2:
        clear()
        menu_playlists()
    elif menu_minhas_playlists == 3:
        clear()
        menu_user()


def menu_minhas_playlists_musicas():
    menu_minhas_playlists_musicas = input_numero("\nMenu Minhas Playlists Musicas \n 1. Adicionar Musica \n 2. Remover Musica \n 3. Alterar Status \n 4.Eliminar Playlist \n 5. Voltar \n 6. Main Menu \n\n Opcao: ")
    if not(validate_option(menu_minhas_playlists_musicas, 6, 1)):
        menu_minhas_playlists_musicas()

    if menu_minhas_playlists_musicas == 1:
        print("#sql adicionar musica")
        nome_musica = input("Nome da musica: ")
    elif menu_minhas_playlists_musicas == 2:

        print("#sql remover musica")
    elif menu_minhas_playlists_musicas == 3:
        print("#sql Alterar Status")
    elif menu_minhas_playlists_musicas == 4:
        print("#sql eliminar playlist")
    elif menu_minhas_playlists_musicas == 5:
        clear()
        menu_playlists()
    elif menu_minhas_playlists_musicas == 6:
        clear()
        menu_user()


def menu_playlists_publicas():
    menu_playlists_publicas = input_numero("\nMenu Playlists Publicas \n 1. Introduzir nome da playlist \n 2. Main Menu \n\n Opcao: ")
    if not(validate_option(menu_playlists_publicas, 2, 1)):
        menu_playlists_publicas()

    if menu_playlists_publicas == 1:
        print("#sql")
    elif menu_playlists_publicas == 2:
        clear()
        menu_user()


def menu_criar_playlist():
    print("Menu Criar Playlist")
    nome_da_playlist=input("\n Nome da Playlist: ")
    publica=("\n Tornar Publica: ")
    menu_minhas_playlists()


def menu_concertos():
    print("Menu Concertos")
    menu_concertos = input_numero("\nMenu Concertos \n 1. Introduzir nome do concerto \n 2. Main Menu \n\n Opcao: ")
    if not(validate_option(menu_concertos, 2, 1)):
        menu_concertos()
    if menu_concertos == 1:
        input("Nome do Concerto: ")
        #sql
    elif menu_concertos == 2:
        clear()
        menu_user()

def menu_editar_periodos():
    menu_periodos = input_numero("\nMenu Periodos \n 1. Criar Periodo \n 2. Eliminar Periodo \n 3. Editar Periodo \n 4. Menu \n\n Opcao: ")
    if not (validate_option(menu_periodos, 4, 1)):
        menu_editar_periodos()

    if menu_periodos == 1:
        print("sql criar periodo")
    elif menu_periodos == 2:
        print("sql eliminar periodo")
    elif menu_periodos == 3:
        print("sql editar periodo")
    elif menu_periodos == 4:
        clear()
        menu_user()

def menu_adicionar_playlist(musica):
    nome_playlist=input("Nome da playlist a inserir a musica %s: "%(musica))
    #sql


def menu_ouvir(musica):
    print("A ouvir" + musica)
    #mixer.init()
    #mixer.music.load(menu_ouvir(musica))  #ficheiro da musica
    #mixer.music.play()

#ouvir ? fazer download ler ficheiro



clear()

drop_music()
