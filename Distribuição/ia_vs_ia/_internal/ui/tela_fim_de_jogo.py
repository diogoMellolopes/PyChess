# Imports necessários
import sys
import os
from PyQt5.QtWidgets import (
    QVBoxLayout, QPushButton, QWidget,
    QLabel, QApplication, QDialog, QHBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

CAMINHO_ASSETS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets"))

class TelaFimDeJogo(QWidget):
    """
    Classe TelaFimDeJogo, herdando QWidget

    Exibe a tela de encerramento da partida de xadrez.
    Permite o jogador começar uma nova partida, ou sair da interface.
    """

    def __init__(self, mensagem_fim, interface_original):
        """
        Inicializa e configura a tela gráfica exibida ao ser finalizado o jogo de Xadrez.

        Args:
            mensagem_fim (str): Mensagem a ser exibida ao jogador (ex: "Xeque-mate", "Empate").
            interface_original (QWidget): Classe da interface principal do jogo, usada para reiniciar.
        """

        super().__init__()
        self.interface_original = interface_original
        self.callback_sair = QApplication.instance().quit

        self.setWindowTitle("Fim de Jogo")
        self.setFixedSize(960, 640)
        self.setStyleSheet("background-color: #1d2a20;")

        layout_principal = QVBoxLayout()
        layout_principal.setAlignment(Qt.AlignCenter)
        layout_principal.setSpacing(40)

        # Criação do label para exibir a mensagem de fim de jogo
        self.label_mensagem = QLabel(mensagem_fim)
        self.label_mensagem.setStyleSheet("color: #EEE8D5; font-size: 48px; font-weight: bold;")
        self.label_mensagem.setFont(QFont("Georgia", 18, QFont.Bold))
        self.label_mensagem.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(self.label_mensagem)

        layout_botoes = QVBoxLayout()
        layout_botoes.setSpacing(10)
        layout_botoes.setAlignment(Qt.AlignCenter)

        # Criação do botão de nova partida
        self.botao_nova_partida = QPushButton()
        caminho_normal = os.path.join(CAMINHO_ASSETS, "botao_rejogar.png").replace("\\", "/")
        caminho_hover = os.path.join(CAMINHO_ASSETS, "botao_rejogar_hover.png").replace("\\", "/")
        caminho_pressed = os.path.join(CAMINHO_ASSETS, "botao_rejogar_pressed.png").replace("\\", "/")
        self.botao_nova_partida.setFixedSize(240, 120)
        self.botao_nova_partida.setStyleSheet(f"""
            QPushButton {{
                border: none;
                background-color: transparent;
                background-image: url("{caminho_normal}");
            }}
            QPushButton:hover {{
                background-image: url("{caminho_hover}");
            }}
            QPushButton:pressed {{
                background-image: url("{caminho_pressed}");
            }}
        """)
        self.botao_nova_partida.clicked.connect(self.nova_partida)
        layout_botoes.addWidget(self.botao_nova_partida, alignment=Qt.AlignCenter)

        # Criação do botão de para sair da interface
        self.botao_sair = QPushButton()
        caminho_normal = os.path.join(CAMINHO_ASSETS, "botao_sair.png").replace("\\", "/")
        caminho_hover = os.path.join(CAMINHO_ASSETS, "botao_sair_hover.png").replace("\\", "/")
        caminho_pressed = os.path.join(CAMINHO_ASSETS, "botao_sair_pressed.png").replace("\\", "/")
        self.botao_sair.setFixedSize(240, 120)
        self.botao_sair.setStyleSheet(f"""
            QPushButton {{
                border: none;
                background-color: transparent;
                background-image: url("{caminho_normal}");
            }}
            QPushButton:hover {{
                background-image: url("{caminho_hover}");
            }}
            QPushButton:pressed {{
                background-image: url("{caminho_pressed}");
            }}
        """)
        self.botao_sair.clicked.connect(self.sair)
        layout_botoes.addWidget(self.botao_sair, alignment=Qt.AlignCenter)

        layout_principal.addLayout(layout_botoes)
        self.setLayout(layout_principal)

    def nova_partida(self):
        """
        Método integrado ao botão de nova partida.
        Ao ser chamado permite o jogador escolher a cor do seu próximo jogo.
        """

        self.escolher_cor()
    
    def escolher_cor(self):
        """
        Configura a tela gráfica modal, que permite o jogador selecionar qual cor deseja jogar (branco ou preto).
        Assim que for escolhido, se inicia um novo jogo com base na escolha.
        """

        resultado = None
        dialog = QDialog(self)
        dialog.setWindowTitle("Escolha de Cor")
        dialog.setModal(True)

        layout = QVBoxLayout()

        # Criação do label
        label = QLabel("Com qual cor você deseja jogar?")
        label.setStyleSheet("color: #EEE8D5; font-size: 18px; font-family: 'Georgia'; font-weight: bold;")
        layout.addWidget(label)

        button_layout = QHBoxLayout()

        # Criação do botão para escolher as brancas
        branco = QPushButton("Brancas")
        branco.setStyleSheet("""
            QPushButton {
                background-color: #586E57;
                color: #EEE8D5; 
                border: none;
                padding: 6px 12px;
                border-radius: 5px;
                font-size: 16px;
                font-family: 'Georgia';
            }
            QPushButton:hover {
                background-color: #6B8E65; /* Cor ao passar o mouse */
            }
        """)

        # Criação do botão para escolhar as pretas
        preto = QPushButton("Pretas")
        preto.setStyleSheet("""
            QPushButton {
                background-color: #586E57;
                color: #EEE8D5; 
                border: none;
                padding: 6px 12px;
                border-radius: 5px;
                font-size: 16px;
                font-family: 'Georgia';
            }
            QPushButton:hover {
                background-color: #6B8E65; /* Cor ao passar o mouse */
            }
        """)
        
        button_layout.addWidget(branco)
        button_layout.addWidget(preto)
        layout.addLayout(button_layout)
        dialog.setLayout(layout)

        def escolher_branco():
            """
            Define a cor branca como escolha e fecha o diálogo.
            """

            nonlocal resultado
            resultado = 0
            dialog.accept()
        
        def escolher_preto():
            """
            Define a cor preta como escolha e fecha o diálogo.
            """

            nonlocal resultado
            resultado = 1
            dialog.accept()
        
        branco.clicked.connect(escolher_branco)
        preto.clicked.connect(escolher_preto)
        
        # Verifica se o jogador escolheu umas das duas opções e inicia o jogo
        if dialog.exec_() == QDialog.Accepted and resultado is not None:
            self.cor_jogador = resultado
            nova_janela = self.interface_original(resultado)
            nova_janela.show()
            self.close()

    def sair(self):
        """
        Fecha a interface e encerra a aplicação.
        """

        self.close()
        self.callback_sair()