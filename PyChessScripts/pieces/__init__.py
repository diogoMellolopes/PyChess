"""
Módulo de Peças de Xadrez

Contém as classes que representam todas as peças do Xadrez.
Cada classe define o seu comportamento específico de movimentação, bem como os seus atributos.

Classes disponíveis:
    - Piece: Classe base para as demais peças.
    - Pawn: Peão
    - Rook: Torre
    - Bishop: Bispo
    - Horse: Cavalo
    - Queen: Rainha
    - King: Rei

As classes podem ser importadas diretamente deste pacote para facilitar o uso:
    from pieces import *

Cada peça implementa o método ".movimento(tabuleiro)" método comum a todas elas
e que serve para atualizar os movimentos válidos de acordo com a sua posição e o
estado atual do tabuleiro.
"""

from .pawn import Pawn
from .rook import Rook
from .bishop import Bishop
from .horse import Horse
from .queen import Queen
from .king import King
from .piece import Piece

__all__ = ["Pawn", "Rook", "Bishop", "Horse", "Queen", "King", "Piece"]