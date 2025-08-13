"""
Módulo da interface do jogo de Xadrez.

Contém as classes e os módulos relacionados à interface gráfica do jogo de Xadrez (PyChess),
incluindo janela, widgets e componentes visuais.

Módulos principais:
    - casalabel.py: Define a classe CasaLabel, responsável por representar as casas do tabuleiro.
    - promocao_widget.py: Define a classe PromocaoWidget, usada para selecionar uma peça, ao promover um peão.
    - tela_fim_de_jogo.py: Define a classe TelaFimDeJogo, exibida no término da partida.
    - menu.py: Define a tela de ínicio (MenuWindow).
    - interface.py: Define a janela principal do jogo (MainWindow).

As classes podem ser importadas diretamente deste pacote para facilitar o uso:
    from ui import *
"""

from .casalabel import CasaLabel
from .promocao_widget import PromocaoWidget
from .tela_fim_de_jogo import TelaFimDeJogo
from .menu import MenuWindow
from .interface import MainWindow

__all__ = ["CasaLabel", "PromocaoWidget", "TelaFimDeJogo", "MenuWindow", "MainWindow"]