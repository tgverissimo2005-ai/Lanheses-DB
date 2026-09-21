from datetime import datetime
opcoes = """=== Lanheses DB ===

1. Ver jogadores
2. Adicionar jogador
3. Sair
"""
print(opcoes)
while True: #faz repetir até achar um break, fazemos isso pq assim nao precisamos de uma condicao no while
    try:
        opcao_escolhida = int(input("Escolha uma opção: ")) #input guarda um str e nao um int, entao transformamos manualmente
        if opcao_escolhida not in [1,2,3]:
            print("Escolha uma opção válida")
        else: 
            break #sai do while quando o input é uma opcao válida (1,2,3)       
    except ValueError:
        print("Escolha um número válido")

if opcao_escolhida == 1:
    # abre uma aba com a lista de jogadores ja adicionados na base de dados
    print("Ver jogadores")

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

    lista_pos = ["Guarda-redes", "Lateral Direito", "Ala Direito", "Defesa Central", "Lateral Esquerdo", "Ala Esquerdo", "Médio Defensivo", "Médio Centro", "Médio Ofensivo", "Extremo Direito", "Extremo Esquerdo", "Ponta de Lança"]
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
            texto = input("Escolha asposições secundárias: ")
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
elif opcao_escolhida == 3:
    print("Até logo!")

