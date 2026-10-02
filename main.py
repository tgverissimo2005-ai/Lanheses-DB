from datetime import datetime
import sqlite3
import textwrap #para ajudar visualmente e esteticamente na demonstracao das posicoes secundarias
bd_lanheses = sqlite3.connect("lanheses.db") #criamos a ligacao com a base de dados e guardamo-la na var bd_lanheses
cursor = bd_lanheses.cursor() #criamos um cursor que ira mandar comandos SQL à BD
cursor.execute("""
CREATE TABLE IF NOT EXISTS jogadores(
id INTEGER PRIMARY KEY,
nome TEXT,
numero INTEGER,
pos_prin TEXT,
data_nascimento DATE,
pe_dom TEXT
)
""") #criamos a tabela jogadores apenas se ela ja nao existir, com as colunas id, nome,...

cursor.execute("""
CREATE TABLE IF NOT EXISTS posicoes_sec(
id INTEGER PRIMARY KEY,
id_jogador INTEGER,
posicao_sec TEXT,
FOREIGN KEY (id_jogador) REFERENCES jogadores(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS nacionalidades(
id INTEGER PRIMARY KEY,
id_jogador INTEGER,
nacionalidade TEXT,
FOREIGN KEY (id_jogador) REFERENCES jogadores(id)
)
""")

opcoes = """=== Lanheses DB ===

1. Ver jogadores
2. Adicionar jogador
3. Remover jogador
4. Editar jogador
5. Sair
"""
#===============================================================================================================================================================================================================================================
# === VARIAVEIS GLOBAIS ===
lista_pos = ["Guarda-redes", "Lateral Direito", "Ala Direito", "Defesa Central", "Lateral Esquerdo", "Ala Esquerdo", "Médio Defensivo", "Médio Centro", "Médio Ofensivo", "Extremo Direito", "Extremo Esquerdo", "Ponta de Lança"]
lista_nacionalidades = ["Português", "Brasileiro", "Angolano", "Francês", "Argentino", "Espanhol", "Cabo Verdiano"]
lista_pes = ["Direito", "Esquerdo", "Ambos"]
lista_guarda_redes = ["Guarda-redes"]
lista_defesas = ["Lateral Direito", "Ala Direito", "Defesa Central", "Lateral Esquerdo", "Ala Esquerdo"]
lista_medios = ["Médio Defensivo", "Médio Centro", "Médio Ofensivo"]
lista_avancados = ["Extremo Direito", "Extremo Esquerdo", "Ponta de Lança"]
#===============================================================================================================================================================================================================================================


#===============================================================================================================================================================================================================================================
# === FUNÇÕES ===

def mostrar_jogadores(categoria, lista,jogadores):
    print("\n")
    print(categoria)
    print(161*"-")
    print(f"{'ID':<4}{'Nome':<30}{'Nº':<4}{'Posição':<20}{'Data Nasc':<15}{'Pé':<11}{'Posições Secundárias':<50}{'Nacionalidades':<30}")
    print(161*"-")
    for jogador in jogadores:
        if jogador[3] in lista:
            cursor.execute("""
            SELECT posicao_sec
            FROM posicoes_sec
            WHERE id_jogador = ?
            """,(jogador[0],))
            posicoes_sec = cursor.fetchall()


            cursor.execute("""
            SELECT nacionalidade
            FROM nacionalidades
            WHERE id_jogador = ?
            """,(jogador[0],))
            nacionalidades = cursor.fetchall()


            nomes_posicoes = []
            for i in posicoes_sec:
                nomes_posicoes.append(i[0]) #vai guardar as posicoes secundarias em uma lista para cada jogador
            posicoes_sec_texto = ", ".join(nomes_posicoes)

            #pega em posicoes_sec_texto e divide em varias strings, tendo cada uma no maximo 50 caracteres
            linhas_posicoes = textwrap.wrap(posicoes_sec_texto, width=50)
            #caso nao tenha posicoes secundarias, linhas_posicoes fica com "" para nao dar IndexError
            if not linhas_posicoes:
                linhas_posicoes = [""]

            nomes_nacionalidades = []
            for j in nacionalidades:
                nomes_nacionalidades.append(j[0])
            nacionalidades_texto = ", ".join(nomes_nacionalidades)

            
            data_formatada = datetime.strptime(jogador[4], "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y")
            #print(",".join( str(elem) for elem in jogador))
            #ficava tudo junto e feio, vamos deixar mais bonito
            print(f"{jogador[0]:<4}{jogador[1]:<30}{jogador[2]:<4}{jogador[3]:<20}{data_formatada:<15}{jogador[5]:<12}{linhas_posicoes[0]:<50}{nacionalidades_texto:<30}")
            espacos = " "*85
            for linha in linhas_posicoes[1:]: #pega em todas as linhas a partir da segunda
                print(f"{espacos}{linha:<50}") #da espacos ate chegar a coluna das posicoes secundarias

def ver_jogadores(pausa=True):
    # abre uma aba com a lista de jogadores ja adicionados na base de dados
    if pausa:
        print("\n")
        print("=== Ver Jogadores ===")
    cursor.execute("""
    SELECT * FROM jogadores
    """)
    jogadores = cursor.fetchall() #pega em todos os resultados e coloca-os na var jogadores
    #jogadores fica entao como uma lista de tuplos, cada um destes tuplos tem os atributos dos jogadores
    mostrar_jogadores("GUARDA-REDES",lista_guarda_redes,jogadores)
    mostrar_jogadores("DEFESAS",lista_defesas,jogadores)
    mostrar_jogadores("MÉDIOS",lista_medios,jogadores)
    mostrar_jogadores("AVANÇADOS",lista_avancados,jogadores)
    if pausa:
        #este input serve apenas para o user poder controlar quando volta para o menu
        input("\nPrima ENTER para voltar ao menu")


def adicionar_jogador():
    # abre uma aba com um formulário a preencher para criar a ficha de um jogador na base de dados
    print("=== Adicionar Jogador ===")
    
    nome = input("Nome (0 para cancelar): ")
    if nome == "0":
        return
    while True:
        try:
            numero = int(input("Número: "))
            if numero not in range(1,100):
                print("Escolha um número de 1 a 99")
            else:    
                break
        except ValueError:
            print("Escolha um número válido")

    print("Posição principal: ")
    for num, posicao in enumerate(lista_pos, start=1):
        print(num, posicao)
    while True:
        try:
            pos_escolhida = int(input("Escolha: "))
            if pos_escolhida not in range(1,len(lista_pos)+1):
                print("Escolha uma posição válida")
            else: 
                pos = lista_pos[pos_escolhida-1] # o indice da lista comeca no 0, entao temos que colocar o -1 para ajustar ao numero mostrado ao utilizador
                break
        except ValueError:
            print("Escolha um número válido")
    while True:
        try:
            posicoes_secundarias = [] #criamos a lista vazia primeiro
            entrada_valida = True #flag para saber se podemos sair do while ou nao
            texto = input("Escolha as posições secundárias: ")
            if texto == "": # caso o user nao selecione nenhuma pos sec, fazemos break e saimos do while
                break
            escolhas = texto.split(",")
            for e in escolhas:
                e = int(e)
                if e not in range(1,len(lista_pos)+1):
                    print("Escolha números válidos")
                    entrada_valida = False
                    break # se encontramos um numero invalido nao precisamos percorrer os outros, podemos sair diretamente do for
                else:
                    posicoes_secundarias.append(lista_pos[e-1])
        except ValueError:
            print("Escolha números válidos")
            entrada_valida = False
        if entrada_valida == True:
            break
    while True:
        try:
            data_nascimento = input("Data de nascimento (DD/MM/AAAA): ")
            data_nascimento = datetime.strptime(data_nascimento, "%d/%m/%Y")
            break
        except ValueError:
            print("Insira uma data válida")

    print("Nacionalidades:")
    for num, nacionalidade in enumerate(lista_nacionalidades, start=1):
        print(num, nacionalidade)
    while True:
        try:
            nacionalidades_escolhidas= []
            entrada_valida = True
            texto = input("Escolha os números correspondentes às nacionalidades: ")
            escolhas_nac = texto.split(",")

            for n in escolhas_nac:
                n = int(n)
                if n not in range(1,len(lista_nacionalidades)+1):
                    entrada_valida = False
                    break #para sairmos do for
                else:
                    nacionalidades_escolhidas.append(lista_nacionalidades[n-1])

        except ValueError:
            print("Escolha nações válidas")
            entrada_valida = False

        if entrada_valida==True:
            break
    print("Pé dominante: ")
    for (num,p) in enumerate(lista_pes, start=1):
        print(num,p)
    while True:
        try:
            pe_dominante = int(input("Escolha o número correspondente ao pé dominante: "))
            if pe_dominante in range(1,len(lista_pes)+1):
                pe_dominante = lista_pes[pe_dominante-1]
                break
            else:
                print("Escolha um número válido")
        except ValueError:
            print("Escolha uma opção válida")

    #=====================================================================
    #INSERIR NAS TABELAS
    #colocamos os atributos do jogador na base de dados
    #colocamos ? em VALUES porque o SQLite nao interpreta diretamente as variaveis Python
    #os valores das variaveis sao passados depois como parametros
    cursor.execute("""
    INSERT INTO jogadores (nome,numero,pos_prin, data_nascimento, pe_dom)
    VALUES(?,?,?,?,?)
    """, (nome, numero, pos, data_nascimento, pe_dominante))

    ultimo_id = cursor.lastrowid

    for i in posicoes_secundarias:
        cursor.execute("""
        INSERT INTO posicoes_sec(id_jogador,posicao_sec)
        VALUES(?,?)
        """, (ultimo_id,i))
    for j in nacionalidades_escolhidas:
        cursor.execute("""
        INSERT INTO nacionalidades(id_jogador,nacionalidade)
        VALUES(?,?)
        """, (ultimo_id,j))

    bd_lanheses.commit() #serve para confirmar a alteração na BD
    #=====================================================================

    print("===================================================")
    print("=== Ficha do Jogador ===")
    print("Nome: ", nome)
    print("Número: ", numero)
    print("Posição Principal: ", pos)
    #print("Posições Secundárias: ")
    #for i in posicoes_secundarias:
    #    print(i)
    print("Posições secundárias: ", ", ".join(posicoes_secundarias))

    print("Data de Nascimento: ", data_nascimento)
    #print("Nacionalidades: ")
    #for j in nacionalidades_escolhidas:
        #print(j)
    print("Nacionalidades: ", ", ".join(nacionalidades_escolhidas))
    print("Pé dominante: ", pe_dominante)
    print("===================================================")

    input("\nPrima ENTER para voltar ao menu")

def remover_jogador():
    print("=== Remover Jogador ===")
    print(f"{'ID':<4}{'Nome':<30}{'Nº':<4}")

    cursor.execute("""
    SELECT id, nome, numero FROM jogadores
    """)

    jogadores = cursor.fetchall()
    for jogador in jogadores:
        print(f"{jogador[0]:<4}{jogador[1]:<30}{jogador[2]:<4}")
        #print(",".join( str(elem) for elem in jogador))

    #criamos uma lista com os ids de cada jogador para depois podermos fazer a validacao da escolha do user
    #jogador[0] é o id do jogador
    ids = [jogador[0] for jogador in jogadores]
    while True:
        try:
            id_escolhido = int(input("\nEscolhe o ID do jogador a remover (Escolha 0 para cancelar): "))
            if id_escolhido not in ids:
                if id_escolhido == 0:
                    print("Operação cancelada\n")
                    break
                else:
                    print("Escolha um ID válido")
            else:
                cursor.execute("""
                DELETE FROM jogadores
                WHERE id = ?
                """, (id_escolhido,))

                cursor.execute("""
                DELETE FROM posicoes_sec
                WHERE id_jogador = ?
                """,(id_escolhido,))

                cursor.execute("""
                DELETE FROM nacionalidades
                WHERE id_jogador = ?
                """,(id_escolhido,))

                bd_lanheses.commit()
                break
        except ValueError:
            print("Escolha um ID válido")

def editar_jogador():
    #vamos mostrar os jogadores na BD sem o input de voltar ao menu
    #pedimos o id
    #validamos o id
    #mostrar atribs e validar escolha
    print("\n")
    print("=== Editar Jogador ===")
    ver_jogadores(pausa=False)

    while True:
        try:
            jogador_editar = int(input("\nEscolha o ID do jogador a alterar (0 para cancelar): "))
            print("\n")
            cursor.execute("""
            SELECT id FROM jogadores
            """)
            ids = cursor.fetchall()
            #transformamos a lista ids que era uma lista de tuplos, em uma lista de int apenas com os ids
            ids = [id[0] for id in ids]

            cursor.execute("""
            SELECT nome FROM jogadores
            WHERE id = ?
            """, (jogador_editar,))

            if jogador_editar == 0:
                return
            elif jogador_editar not in ids:
                print("Escolha um ID válido: ")
            else:
                nome_selecionado_tuplo = cursor.fetchone()
                nome_selecionado = nome_selecionado_tuplo[0]

                break
        except ValueError:
            print("Escolha um ID válido")

    
    print (f"Jogador selecionado: {nome_selecionado}")
    
    while True:
        atributos = """
    ATRIBUTOS:
            1. Nome
            2. Número
            3. Posição
            4. Data de Nascimento
            5. Pé dominante
            6. Posições Secundárias
            7. Nacionalidades
            0. Terminar
            """
        print(atributos)
        while True:
            try:
                atrib_escolhido = int(input("\nEscolha o atributo a alterar: "))
                print("\n")
                if atrib_escolhido not in range (0,8):
                    print("Escolha uma opção válida")
                else:
                    break
            except ValueError:
                print("Escolha um número válido")
        
        if atrib_escolhido == 0:
            return
        
        if atrib_escolhido == 1:
            coluna = "nome"
            nome_atributo = "Nome"

        elif atrib_escolhido == 2:
            coluna = "numero"
            nome_atributo = "Número"

        elif atrib_escolhido == 3:
            coluna = "pos_prin"
            nome_atributo = "Posição"
            
        elif atrib_escolhido == 4:
            coluna = "data_nascimento"
            nome_atributo = "Data de nascimento"
            ""
            
        elif atrib_escolhido == 5:
            coluna = "pe_dom"
            nome_atributo = "Pé dominante"

        elif atrib_escolhido == 6:

            cursor.execute("""
            SELECT posicao_sec
            FROM posicoes_sec
            WHERE id_jogador = ?
            """, (jogador_editar,))

            posicoes_sec_atuais = cursor.fetchall()
            nomes_posicoes = []

            #este for vai vai transformar a lista de tuplos(vinda do fetchall()) em uma lista de textos
            for i in posicoes_sec_atuais:
                nomes_posicoes.append(i[0])
            print("Posições secundárias atuais: ")

            #este for pega na lista e apresenta as pos sec de forma enumerada
            for num,pos in enumerate(nomes_posicoes,start=1):
                print(num, pos)

            print("\n")
            print(20*"-")
            print("\n")
            print("Opções:")

            #este for mostra ao user as opcoes de posicoes
            for num,pos in enumerate(lista_pos, start=1):
                print(num,pos)

            #pedir ao user as novas posicoes sec e colocar na lista novas_pos_sec
            #e tambem verificar se o user selecionou pos sec ou nao
            while True:
                entrada_valida = True #usada como flag para saber se os numeros que o user inseriu sao validos, permitindo-nos sair do while
                try:
                    print("\n")
                    novas_pos_sec_texto = input("Posições secundárias novas: ")
                    print("\n")
                    
                    if novas_pos_sec_texto == "":
                        novas_pos_sec = []
                    else:
                        novas_pos_sec = novas_pos_sec_texto.split(",")

                    #transforma os itens da lista de texto para int
                    novas_pos_sec_int = []
                    for j in novas_pos_sec:
                        novas_pos_sec_int.append(int(j))

                    for n in novas_pos_sec_int:
                        if n not in range(1,len(lista_pos)+1):
                            entrada_valida = False
                            print("Escolha opções válidas")
                            break
                        else:
                            entrada_valida = True

                    novas_pos_final = []
                    if entrada_valida:
                        for k in novas_pos_sec_int:
                            novas_pos_final.append(lista_pos[k-1])
                        break
                except ValueError:
                    print("Escolha números válidos")

            #eliminar as posicoes secundarias que tinhamos na bd para o jogador a editar
            cursor.execute("""
            DELETE 
            FROM posicoes_sec
            WHERE id_jogador = ?
            """,(jogador_editar,))


            #adicionar as posicoes secundarias novas
            for l in novas_pos_final:
                cursor.execute("""
                INSERT INTO posicoes_sec(id_jogador,posicao_sec)
                VALUES(?,?)
                """, (jogador_editar,l))

            bd_lanheses.commit()
            #retiramos daqui o return pois com a nossa decisao de colocar a edicao do mesmo jogador em loop ate o user digitar 0, entao substituimos esse return por um continue, que passa diretamente para a proxima iteracao do loop e ignora o select da tabela jogadores
            #return # temos que colocar o return dentro do elif para ele nao seguir o fluxo na funcao e se deparar com a pesquisa SELECT ... FROM jogadores
            continue

        elif atrib_escolhido == 7:
            cursor.execute("""
            SELECT nacionalidade
            FROM nacionalidades
            WHERE id_jogador = ?
            """,(jogador_editar,))

            nacionalidades_atuais = cursor.fetchall()
            nomes_nacionalidades = []

            #transformar em lista de textos
            for nac in nacionalidades_atuais:
                nomes_nacionalidades.append(nac[0])

            print("Nacionalidades atuais:")
            #printar as nacionalidades atuais do jogador
            for num,nac in enumerate(nomes_nacionalidades, start=1):
                print(num, nac)

            #mostrar as opcoes ao user
            print("\n")
            print(20*"-")
            print("\n")
            print("Opções:")
            for num,opc in enumerate(lista_nacionalidades,start=1):
                print(num,opc)

            while True:
                entrada_valida = True
                try:
                    print("\n")
                    novas_nac_texto = input("Novas nacionalidades: ")
                    print("\n")
                    if novas_nac_texto == "":
                        novas_nac = []
                    else:
                        novas_nac = novas_nac_texto.split(",")

                    #guardar como ints as nacionalidades
                    novas_nac_int = []
                    for txt in novas_nac:
                        novas_nac_int.append(int(txt))

                    for n in novas_nac_int:
                        if n not in range(1,len(lista_nacionalidades)+1):
                            entrada_valida = False
                            print("Escolha opções válidas")
                            break
                        else:
                            entrada_valida = True

                    #transformar os ints nas nacs correspondentes
                    novas_nac_final =[]
                    if entrada_valida:
                        for i in novas_nac_int:
                            novas_nac_final.append(lista_nacionalidades[i-1])
                        break
                except ValueError:
                    print("Escolha números válidos")
            #eliminar as nacionalidades antigas
            cursor.execute("""
            DELETE
            FROM nacionalidades
            WHERE id_jogador = ?
            """, (jogador_editar,))

            #adicionar novas nacionalidades
            for nac in novas_nac_final:
                cursor.execute("""
                INSERT INTO nacionalidades(id_jogador,nacionalidade)
                VALUES(?,?)
                """,(jogador_editar,nac))

            #salvar as alteracoes
            bd_lanheses.commit()

            #retiramos o return para nao sair do loop e substituimos por um continue para ignorar o select da tabela jogadores
            #return
            continue


        cursor.execute(f"""
        SELECT {coluna} FROM jogadores
        WHERE id = ?
        """,(jogador_editar,))
        #o fetchone retorna ("Thiago Verissimo",) entao fazemos valor_atual = valor_atual_tuplo[0] para retirar apenas o "Thiago Verissimo"
        valor_atual_tuplo = cursor.fetchone()
        valor_atual = valor_atual_tuplo[0]
        print(f"{nome_atributo} atual: {valor_atual}")


        # === PEDIR NOVOS ATRIBUTOS ===
        if atrib_escolhido == 1:
            atrib_novo = input("Novo nome: ")

        elif atrib_escolhido == 2:
            while True:
                try:
                    atrib_novo = int(input("Novo número: "))

                    if atrib_novo not in range(1,100):
                        print("Escolha um número de 1 a 99")
                    else:
                        break
                except ValueError:
                    print("Escolha um número válido")

        elif atrib_escolhido == 3:
            for num, posicao in enumerate(lista_pos, start=1):
                print(num, posicao)
            while True:
                try:
                    pos_esc = int(input("Nova posição: "))
                    if pos_esc not in range(1,len(lista_pos)+1):
                        print("Escolha uma opção válida")
                    else:
                        atrib_novo = lista_pos[pos_esc-1]
                        break
                except ValueError:
                    print("Escolha uma posição válida")

        elif atrib_escolhido == 4:
            while True:
                try:
                    atrib_novo = input("Nova data de nascimento (DD/MM/AAAA): ")
                    atrib_novo = datetime.strptime(atrib_novo, "%d/%m/%Y")
                    break
                except ValueError:
                    print("Escolha uma data válida")

        elif atrib_escolhido == 5:
            for num, pe in enumerate(lista_pes,start=1):
                print(num,pe)
            while True:
                try:
                    pe_novo = int(input("Novo pé dominante: "))
                    if pe_novo not in range(1,len(lista_pes)+1):
                        print("Escolha uma opção válida")
                    else:
                        atrib_novo = lista_pes[pe_novo-1]
                        break
                except ValueError:
                    print("Escolha um número válido")
        
        cursor.execute(f"""
        UPDATE jogadores SET {coluna} = ?
        WHERE id = ?
        """, (atrib_novo,jogador_editar))

        bd_lanheses.commit()
    



#===============================================================================================================================================================================================================================================


#o while true vai controlar o programa inteiro, para podermos voltar ao menu depois de executar uma operação

while True:
    print(opcoes)
    while True: #faz repetir até achar um break, fazemos isso pq assim nao precisamos de uma condicao no while
        try:
            opcao_escolhida = int(input("Escolha uma opção: ")) #input guarda um str e nao um int, entao transformamos manualmente
            if opcao_escolhida not in [1,2,3,4,5]:
                print("Escolha uma opção válida")
            else: 
                break #sai do while quando o input é uma opcao válida (1,2,3,4)       
        except ValueError:
            print("Escolha um número válido")

    if opcao_escolhida == 1:
        ver_jogadores()

    elif opcao_escolhida == 2:
        adicionar_jogador()

    elif opcao_escolhida == 3:
        remover_jogador()

    elif opcao_escolhida == 4:
        editar_jogador()
        
    elif opcao_escolhida == 5:
        print("Até logo!")
        break

