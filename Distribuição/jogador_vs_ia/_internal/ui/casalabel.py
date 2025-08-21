# Imports necessários
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import pyqtSignal

class CasaLabel(QLabel):
    """
    Classe CasaLabel, herdando de QLabel.

    Representa uma casa do tabuleiro de xadrez. Cada instância pode emitir um sinal
    quando for clicada, informando sua posição.

    Atributos:
        posicao (str): A posição da casa no tabuleiro, ex: "04" (linha 0, coluna 4).
        clicado (pyqtSignal): Sinal emitido ao clicar na casa, envia a posição (str).
    """

    clicado = pyqtSignal(str)

    def __init__(self, posicao):
        """
        Inicializa uma nova casa do tabuleiro.

        Arqs:
            posicao (str): Posição da casa no tabuleiro.
        """

        super().__init__()
        self.posicao = posicao

    def mousePressEvent(self, event):
        """
        Captura o evento de clique do mouse na casa e emite o sinal "clicado"
        com a posição desta casa.
        """

        self.clicado.emit(self.posicao)