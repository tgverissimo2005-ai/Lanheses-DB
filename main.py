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
        else: break #sai do while quando o input é uma opcao válida (1,2,3)       
    except ValueError:
        print("Escolha um número válido")

 
