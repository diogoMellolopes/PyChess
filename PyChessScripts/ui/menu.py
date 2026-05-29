# Imports necessários
from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QLabel, 
    QApplication, QMessageBox, QSpacerItem, QSizePolicy, QDialog, QFileDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QBrush, QPixmap, QIcon
import sys
import os
from .interface import MainWindow

CAMINHO_ASSETS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets"))

class MenuWindow(QMainWindow):
    """
    Classe MenuWindow, herdando QMainWindow

    Exibe a tela de início gráfica ao executar o programa.
    Permite o jogador começar uma nova partida, carregar uma já salva, ou encerrar a execução do programa.
    """

    def __init__(self):
        """
        Inicializa e configura a tela gráfica ao iniciar o programa.
        """

        super().__init__()
        self.cor_jogador = 0

        self.setWindowTitle("PyChess")
        self.setFixedSize(960, 640)
        self.set_background(os.path.join(CAMINHO_ASSETS, "menu_bg.png"))

        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(40, 40, 40, 40)
        layout_principal.setSpacing(20)

        # Carregando o título do programa
        titulo = QLabel()
        pixmap = QPixmap(os.path.join(CAMINHO_ASSETS, "title.png"))
        titulo.setFixedHeight(150)
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setPixmap(pixmap)
        layout_principal.addWidget(titulo, alignment=Qt.AlignHCenter)
        layout_principal.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        layout_botoes = QHBoxLayout()
        layout_botoes.setSpacing(40)
        layout_botoes.setAlignment(Qt.AlignCenter)

        # Criação dos botões
        botao_novo_jogo = self.criar_botao("▶ Nova Partida", self.abrir_jogo)
        botao_carregar = self.criar_botao("💾 Carregar Partida", self.carregar_jogo)
        botao_sair = self.criar_botao("✖ Sair", self.close)

        layout_botoes.addWidget(botao_novo_jogo)
        layout_botoes.addWidget(botao_carregar)
        layout_botoes.addWidget(botao_sair)
        layout_principal.addLayout(layout_botoes)

        container = QWidget()
        container.setLayout(layout_principal)
        container.setStyleSheet("background: transparent;")
        self.setCentralWidget(container)

    def set_background(self, caminho_imagem):
        """
        Define a imagem de fundo da janela principal.

        Args:
            caminho_imagem (str): Caminho absoluto ou relativo da imagem a ser usada como background.
        """

        palette = QPalette()
        pixmap = QPixmap(caminho_imagem).scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        palette.setBrush(QPalette.Window, QBrush(pixmap))
        self.setPalette(palette)

    def criar_botao(self, texto, funcao):
        """
        Cria um botão estilizado com base no texto e na função fornecidos.

        Args:
            texto (str): Texto exibido no botão.
            funcao (function): Função executada ao clicar no botão.
        """

        # Atribuição dos caminhos das imagens dos botões
        normal_path = os.path.join(CAMINHO_ASSETS, "botao_normal.png").replace(os.sep, "/")
        hover_path = os.path.join(CAMINHO_ASSETS, "botao_hover.png").replace(os.sep, "/")
        pressed_path = os.path.join(CAMINHO_ASSETS, "botao_pressed.png").replace(os.sep, "/")

        # Criação e configuração dos botões
        botao = QPushButton(texto)
        botao.setCursor(Qt.PointingHandCursor)
        botao.setStyleSheet(f"""
            QPushButton {{
                background-image: url("{normal_path}");
                background-repeat: no-repeat;
                background-position: center;
                border: none;
                color: #c7c6af;
                font-size: 17px;
                font-weight: bold;
                min-width: 200px;
                min-height: 60px;
                max-width: 200px;
                max-height: 60px;
            }}
            QPushButton:hover {{
                background-image: url("{hover_path}");
            }}
            QPushButton:pressed {{
                background-image: url("{pressed_path}");
            }}
        """)
        botao.clicked.connect(funcao)
        return botao

    def abrir_jogo(self):
        """
        Método integrado ao botão de novo jogo.
        Ao ser chamado permite o jogador escolher a cor do seu próximo jogo.
        """

        self.escolher_cor()

    def carregar_jogo(self):
        """
        Método integrado ao botão de carregar partida.
        Ao ser chamado permite o jogador navegar no seu diretório de pastas, selecionar
        o .json no qual o jogo está salvo, e então carrega-lo.
        """
        
        # Carrega o arquivo selecionado pelo jogador
        caminho_arquivo, _ = QFileDialog.getOpenFileName(self, "Carregar Partida", "./save", "Arquivos JSON (*.json)")
        if not caminho_arquivo:
            return
        
        try:
            # Tenta carrega-lo, em caso de erro retorna
            from game import Game
            game = Game(carregar=True)
            sucesso = game.carregar_partida(caminho_arquivo)
            if not sucesso:
                QMessageBox.warning(self, "Erro", "Não foi possível carregar a partida.")
                return
            
            self.cor_jogador = game.turno % 2
            self.janela_jogo = MainWindow(self.cor_jogador, game)
            self.janela_jogo.desenhar_tabuleiro()
            self.janela_jogo.show()
            self.close()

        except Exception as e:
            QMessageBox.critical(self, "Erro Crítico", f"Ocorreu um erro ao carregar: {e}")

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
        layout.addWidget(label)
        
        button_layout = QHBoxLayout()

        branco = QPushButton("Brancas")
        preto = QPushButton("Pretas")
        
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
            self.janela_jogo = MainWindow(self.cor_jogador)
            self.janela_jogo.show()
            self.close()

# Execução do Menu
def main():
    app = QApplication(sys.argv)
    caminho_icone = os.path.join(CAMINHO_ASSETS, "icone.ico").replace("\\", "/")
    app.setWindowIcon(QIcon(caminho_icone))
    janela = MenuWindow()
    janela.setWindowIcon(QIcon(caminho_icone))
    janela.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()