from datetime import datetime
import sqlite3
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


opcoes = """=== Lanheses DB ===

1. Ver jogadores
2. Adicionar jogador
3. Remover jogador
4. Sair
"""
#===============================================================================================================================================================================================================================================
# === VARIAVEIS GLOBAIS ===
lista_pos = ["Guarda-redes", "Lateral Direito", "Ala Direito", "Defesa Central", "Lateral Esquerdo", "Ala Esquerdo", "Médio Defensivo", "Médio Centro", "Médio Ofensivo", "Extremo Direito", "Extremo Esquerdo", "Ponta de Lança"]
lista_nacionalidades = ["Português", "Brasileiro", "Angolano", "Francês", "Argentino", "Espanhol", "Cabo Verdiano"]
lista_pes = ["Direito", "Esquerdo", "Ambos"]
#===============================================================================================================================================================================================================================================

#o while true vai controlar o programa inteiro, para podermos voltar ao menu depois de executar uma operação
while True:
    print(opcoes)
    while True: #faz repetir até achar um break, fazemos isso pq assim nao precisamos de uma condicao no while
        try:
            opcao_escolhida = int(input("Escolha uma opção: ")) #input guarda um str e nao um int, entao transformamos manualmente
            if opcao_escolhida not in [1,2,3,4]:
                print("Escolha uma opção válida")
            else: 
                break #sai do while quando o input é uma opcao válida (1,2,3,4)       
        except ValueError:
            print("Escolha um número válido")

    if opcao_escolhida == 1:
        # abre uma aba com a lista de jogadores ja adicionados na base de dados
        print("=== Ver jogadores ===")
        print(f"{'ID':<4}{'Nome':<30}{'Nº':<4}{'Posição':<20}{'Data Nasc':<15}{'Pé':<10}")
        cursor.execute("""
        SELECT * FROM jogadores
        """)
        jogadores = cursor.fetchall() #pega em todos os resultados e coloca-os na var jogadores
        #jogadores fica entao como uma lista de tuplos, cada um destes tuplos tem os atributos dos jogadores
        for jogador in jogadores:
            data_formatada = datetime.strptime(jogador[4], "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y")
            #print(",".join( str(elem) for elem in jogador))
            #ficava tudo junto e feio, vamos deixar mais bonito
            print(f"{jogador[0]:<4}{jogador[1]:<30}{jogador[2]:<4}{jogador[3]:<20}{data_formatada:<15}{jogador[5]:<10}")

        #este input serve apenas para o user poder controlar quando volta para o menu
        input("\nPrima ENTER para voltar ao menu")
    elif opcao_escolhida == 2:
        # abre uma aba com um formulário a preencher para criar a ficha de um jogador na base de dados
        print("=== Adicionar jogador ===")
        nome = input("Nome: ")
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
        #INSERIR NA TABELA
        #colocamos os atributos do jogador na base de dados
        #colocamos ? em VALUES porque o SQLite nao interpreta diretamente as variaveis Python
        #os valores das variaveis sao passados depois como parametros
        cursor.execute("""
        INSERT INTO jogadores (nome,numero,pos_prin, data_nascimento, pe_dom)
        VALUES(?,?,?,?,?)
        """, (nome, numero, pos, data_nascimento, pe_dominante))

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


                

            
    elif opcao_escolhida == 3:
        print("=== Remover jogador ===")
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
                    bd_lanheses.commit()
                    break
            except ValueError:
                print("Escolha um ID válido")
        
    elif opcao_escolhida == 4:
        print("Até logo!")
        break

