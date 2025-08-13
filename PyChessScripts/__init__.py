"""
Módulo do jogo de Xadrez.

Contém as classes e os módulos relacionados ao processamento do jogo de Xadrez (PyChess),
incluindo controle de movimentos, controle do tabuleiro, controle da IA e validação de jogadas.

Módulos principais:
    - treinar_ia.py: Define o script, responsável por realizar as partidas IA contra IA.
    - ia.py: Define a classe IA, reponsável por representar a IA, através de Q-Learning, aprender e realizar jogadas.
    - game.py: Define a classe Game, responsável por controlar os estados do jogo, verificar jogadas válidas e se comunicar com a interface.
    - board.py: Define a classe Board, responsável por representar o tabuleiro.
    - jogador_vs_ia.py: Define o script padrão do jogo, onde ele será inicializado.
    - ia_vs_ia.py: Define o script onde a IA irá se enfrentar contra ela mesma.

As classes podem ser importadas diretamente deste pacote para facilitar o uso:
    from ui import *
"""

from .treinar_ia import *
from .ia import *
from .game import *
from .board import *

__all__ = ["IA", "QLearning", "Game", "Board"]