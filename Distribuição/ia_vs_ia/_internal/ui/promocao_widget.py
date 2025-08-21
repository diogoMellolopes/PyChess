# Imports necessários
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, pyqtSignal
import os

class PromocaoWidget(QDialog):
    """
    Classe PromocaoWidget, herdando a classe pai QDialog

    Representa a janela modal exibida quando um peão atinge a última fileira.
    Permite ao jogador escolher a peça para promoção.

    Atributos:
        peca_escolhida (pyqtSignal): Sinal emitido ao selecionar a peça. Emite o nome da peça (str).
    """
    
    peca_escolhida = pyqtSignal(str) 

    def __init__(self, cor):
        """
        Inicializa a janela de seleção de peça.

        Args:
            cor (int): Cor do jogador (0 para branco, 1 para preto). Define qual conjunto de imagens será exibido.
        """

        super().__init__()
        self.cor = "white" if cor == 0 else "black"

        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setModal(True)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(400, 150)
        self.init_ui()

    def init_ui(self):
        """
        Configura a interface gráfica com as opções de peças disponíveis para promoção.
        """

        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        self.setStyleSheet("""
            background-color: #586E57;  
            border: 3px solid #EEE8D5; 
            border-radius: 15px;
        """)

        pecas_layout = QHBoxLayout()
        pecas_layout.setSpacing(20)
        pecas_layout.setAlignment(Qt.AlignCenter)

        def criar_callback(nome_peca):
            """
            Cria e retorna uma função callback que seleciona a peça especificada.

            Args:
                nome_peca (str): Nome da peça a ser promovida.

            Returns:
                function: Função que pode ser conectada ao clique do QLabel correspondente.
            """

            return lambda event: self.selecionar_peca(nome_peca)

        pecas = ["queen", "rook", "bishop", "horse"]
        for nome in pecas:
            label = QLabel()
            caminho = os.path.join(os.path.dirname(__file__), "..", "assets", f"{nome}_{self.cor}_selected.png")
            pixmap = QPixmap(caminho).scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)

            label.setPixmap(pixmap)
            label.setStyleSheet("""
                QLabel {
                    background-color: #586E57;
                    border-radius: 8px;
                    padding: 5px;
                }
                QLabel:hover {
                    background-color: #4B5E4A;
                }
            """)
            label.setAlignment(Qt.AlignCenter)

            label.mousePressEvent = criar_callback(nome)
            pecas_layout.addWidget(label)

        layout.addLayout(pecas_layout)
        self.setLayout(layout)

    def selecionar_peca(self, nome):
        """
        Emite o sinal com o nome da peça escolhida e fecha o diálogo.
        """
        
        self.peca_escolhida.emit(nome)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.close()