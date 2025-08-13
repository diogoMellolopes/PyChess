"""
Script de treinamento IA vs IA.

Executa partidas automáticas entre duas instâncias da IA (uma jogando com as peças brancas, a outra com as pretas),
com o objetivo de treinar e aprimorar o desempenho por meio de algoritmo de Q-Learning.

Processo:
    - Inicializa duas instâncias da IA e um jogo.
    - Executa um número definido de partidas automáticas.
    - Salva periodiacamente a Q_Table com o aprendizado.
"""

# Imports necessários
from game import Game  
from ia import IA      

NUM_JOGOS = 1000 # Número de partidas definidas para treinamento

# Inicialização das classes
jogo = Game()  
ia_branca = IA(jogo, cor_ia=0)
ia_preta = IA(jogo, cor_ia=1)

# Criação do laço responsável por simular o NUM_JOGOS partidas
for n in range(NUM_JOGOS):
    print(f"\n[Partida {n+1}]")
    jogo.reiniciar()  
    fim = False
    jogo.turno = 0

    # Executa jogadas até encontrar condição de término
    while not fim:
        ia_atual = ia_branca if jogo.turno % 2 == 0 else ia_preta
        ia_atual.simular_jogada()

        # Fim do jogo
        if not ia_atual.lista_jogadas_possiveis:
            print("[FIM DA PARTIDA]")
            resultado = ia_atual.esta_em_mate_ou_afogamento(ia_atual.cor)
            print("Resultado:", resultado)
            break

        ia_atual.aplicar_jogada_escolhida()

    if (n+1) % 100 == 0:
        ia_branca.qlearning.salvar_q_table()
        ia_preta.qlearning.salvar_q_table()

# Salvar na q_table o aprendizado
ia_branca.qlearning.salvar_q_table()
ia_preta.qlearning.salvar_q_table()