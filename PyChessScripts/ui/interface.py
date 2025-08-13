# Imports necessários
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QGridLayout, QLabel, QFileDialog, QPushButton, QSizePolicy
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer
from .promocao_widget import PromocaoWidget
from .casalabel import CasaLabel
from .tela_fim_de_jogo import TelaFimDeJogo
import sys  
import os

# Pegando um diretório acima pra importar game e ia
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from game import Game
from ia import IA

TAMANHO_CASA = 80 
CAMINHO_ASSETS = caminho_assets = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets"))

class MainWindow(QMainWindow):
    """
    Classe MainWindow, herdando QMainWindow.

    Janela principal da aplicação de Xadrez.
    Responsável por exibir a interface gráfica, interagir com o usuário,
    atualizar o estado do tabuleiro e controlar a partida.
    """

    def __init__(self, cor_jogador = 0, jogo = None, modo_ia_vs_ia = False):
        """
        Inicializa a janela principal do jogo.

        Args:
            cor_jogador (int): Cor do jogador humano (0 = branco, 1 = preto).
            jogo (Game, opcional): Instância da classe Game. Se não for fornecida, uma nova será criada.
            modo_ia_vs_ia (bool): Se True, ativa o modo IA vs IA.
        """

        super().__init__()

        # Configuração dos principais atributos
        self.jogo = jogo if jogo else Game(cor_ia = 1 - cor_jogador)
        self.modo_ia_vs_ia = modo_ia_vs_ia
        self.jogo_finalizado = 0

        # Verificação da flag
        if self.modo_ia_vs_ia:
            self.ia_branca = IA(self.jogo, cor_ia=0)
            self.ia_preta = IA(self.jogo, cor_ia=1)
        
        self.setWindowTitle("Xadrez")
        self.setFixedSize(960, 700)
        self.setStyleSheet("background-color: #1d2a20;") 

        self.widget_central = QWidget()
        self.setCentralWidget(self.widget_central)

        layout_geral = QHBoxLayout()
        layout_geral.setContentsMargins(0, 0, 0, 0)
        layout_geral.setSpacing(0)
        layout_geral.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.widget_central.setLayout(layout_geral)

        # Criação do painel lateral com a numeração de 8 a 1
        numeracao_lateral = QLabel()
        numeracao_lateral.setFixedSize(60, 700)
        pixmap = QPixmap(os.path.join(CAMINHO_ASSETS, "lateral_esquerda.png"))
        numeracao_lateral.setPixmap(pixmap)
        layout_geral.addWidget(numeracao_lateral)

        tabuleiro_widget = QWidget()
        tabuleiro_widget.setFixedSize(640, 640)

        # Criação do tabuleiro
        self.grid = QGridLayout()
        self.grid.setSpacing(0)
        self.grid.setContentsMargins(0, 0, 0, 0)
        tabuleiro_widget.setLayout(self.grid)

        tabuleiro_com_barra = QVBoxLayout()
        tabuleiro_com_barra.setContentsMargins(0, 0, 0, 0)
        tabuleiro_com_barra.setSpacing(0)
        tabuleiro_com_barra.addWidget(tabuleiro_widget)

        # Criação do painel inferior com o alfabeto de A à H
        barra_inferior = QLabel()
        barra_inferior.setFixedSize(640, 60)
        pixmap_barra = QPixmap(os.path.join(CAMINHO_ASSETS, "lateral_inferior.png")).scaled(640, 60)
        barra_inferior.setPixmap(pixmap_barra)
        tabuleiro_com_barra.addWidget(barra_inferior)

        tabuleiro_widget_container = QWidget()
        tabuleiro_widget_container.setLayout(tabuleiro_com_barra)
        tabuleiro_widget_container.setFixedSize(640, 700)  
        layout_geral.addWidget(tabuleiro_widget_container)

        painel_lateral_h = QHBoxLayout()
        painel_lateral_h.setContentsMargins(0, 0, 0, 0)
        painel_lateral_h.setSpacing(0)

        # Criação da lateral direita, para separar o tabuleiro dos botões
        lateral_direita = QLabel()
        lateral_direita.setFixedSize(15, 700)
        pixmap = QPixmap(os.path.join(CAMINHO_ASSETS, "lateral_direita.png")).scaled(20, 700)
        lateral_direita.setPixmap(pixmap)
        painel_lateral_h.addWidget(lateral_direita)

        # Criação do lugar onde será armazenada as demais informações do jogo
        painel_botoes = QVBoxLayout()
        painel_botoes.setContentsMargins(0, 5, 10, 10)
        painel_botoes.setSpacing(4)

        # Criação da label, responsável por rastrear a última jogada executada
        self.contador_ultimo_lance = QLabel("Última jogada: " + "X" * 30)  
        self.contador_ultimo_lance.setStyleSheet("color: #EEE8D5; font-size: 16px; font-weight: bold;")
        self.contador_ultimo_lance.setWordWrap(True)
        self.contador_ultimo_lance.setFixedWidth(240)
        self.contador_ultimo_lance.setMinimumHeight(50)
        self.contador_ultimo_lance.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.contador_ultimo_lance.setMaximumWidth(240)
        self.contador_ultimo_lance.setText("Última jogada: ")
        painel_botoes.addWidget(self.contador_ultimo_lance)

        # Criação do painel de capturas, responsável por rastrear quais peças estão foram de jogo
        painel_botoes.addLayout(self.criar_painel_capturas())
        painel_botoes.addStretch()

        # Criação do botão salvar, responsável por salvar o estado atual da partida
        self.botao_salvar = QPushButton()
        caminho_normal = os.path.join(CAMINHO_ASSETS, "botao_salvar.png").replace("\\", "/")
        caminho_hover = os.path.join(CAMINHO_ASSETS, "botao_salvar_hover.png").replace("\\", "/")
        caminho_pressed = os.path.join(CAMINHO_ASSETS, "botao_salvar_pressed.png").replace("\\", "/")
        self.botao_salvar.setFixedSize(240, 120)
        self.botao_salvar.setStyleSheet(f"""
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
        self.botao_salvar.clicked.connect(self.salvar_partida)
        painel_botoes.addWidget(self.botao_salvar, alignment=Qt.AlignTop)

        # Criação do botão voltar, responsável por voltar uma jogada
        self.botao_voltar = QPushButton()
        self.botao_voltar.setFixedSize(240, 120)
        caminho_normal = os.path.join(CAMINHO_ASSETS, "botao_voltar.png").replace("\\", "/")
        caminho_hover = os.path.join(CAMINHO_ASSETS, "botao_voltar_hover.png").replace("\\", "/")
        caminho_pressed = os.path.join(CAMINHO_ASSETS, "botao_voltar_pressed.png").replace("\\", "/")
        self.botao_voltar.setStyleSheet(f"""
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
        self.botao_voltar.clicked.connect(self.voltar_jogada)
        painel_botoes.addWidget(self.botao_voltar, alignment=Qt.AlignTop)

        # Criação do botão resetar, responsável por iniciar do zero o jogo
        self.botao_resetar = QPushButton()
        self.botao_resetar.setFixedSize(240, 120)
        caminho_normal = os.path.join(CAMINHO_ASSETS, "botao_resetar.png").replace("\\", "/")
        caminho_hover = os.path.join(CAMINHO_ASSETS, "botao_resetar_hover.png").replace("\\", "/")
        caminho_pressed = os.path.join(CAMINHO_ASSETS, "botao_resetar_pressed.png").replace("\\", "/")
        self.botao_resetar.setStyleSheet(f"""
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
        self.botao_resetar.clicked.connect(self.reiniciar)
        painel_botoes.addWidget(self.botao_resetar, alignment=Qt.AlignTop)

        painel_lateral_h.addLayout(painel_botoes)

        painel_widget = QWidget()
        painel_widget.setFixedSize(260, 700) 
        painel_widget.setLayout(painel_lateral_h)
        painel_widget.setContentsMargins(0, 0, 0, 0)
        layout_geral.addWidget(painel_widget)

        self.casas = {}
        self.criar_tabuleiro()
        self.desenhar_tabuleiro()

        # Criação das demais métricas
        self.posicoes_a_limpar = []
        self.posicao_ultima_jogada_a_limpar = []
        self.ultima_jogada_a_limpar = []
        self.ultima_peca_selecionada = 0
        self.cor_jogador = cor_jogador
        self.cor_atual = self.jogo.turno % 2
        self.promocao_em_andamento = 0
        self.empate_por_material_insuficiente = 0
        self.rei_branco_xeque = 0
        self.rei_preto_xeque = 0

        if self.modo_ia_vs_ia:
            QTimer.singleShot(500, self.jogar_ia_vs_ia)
        elif self.cor_atual != self.cor_jogador:
            QTimer.singleShot(200, self.jogar_ia)

    def atualizar_ultimo_lance(self):
        """
        Atualiza o texto da última jogada exibida no painel lateral.

        Traduz a notação interna da jogada mais recente para uma
        descrição em português e a exibe no QLabel correspondente.
        """

        jogada = "Última jogada: "
        xeque = False
        ignorar = False
        if len(self.jogo.historico) == 0:
            self.contador_ultimo_lance.setText(jogada)
            return
        
        # Pega a última jogada do histórico do jogo
        ultimo_lance = self.jogo.historico[self.jogo.turno - 1]

        # Visualiza a peça
        peca_jogada = ultimo_lance[0]
        pecas_possiveis = {"P":"Peão", "R":"Torre", "H":"Cavalo", "B":"Bispo", "Q":"Rainha", "K":"Rei"}
        peca = pecas_possiveis.get(peca_jogada)

        # Visualiza a cor
        cor = ultimo_lance[1]
        if cor == "b":
            if peca == "Rainha" or peca == "Torre":
                cor = "Branca"
            else:
                cor = "Branco"
        else: 
            if peca == "Rainha" or peca == "Torre":
                cor = "Preta"
            else:
                cor = "Preto"

        # Armazena
        jogada += peca + " " + cor + " " + "de "

        # Visualiza a posição
        posicao_passada_x = int(ultimo_lance[2])
        posicao_passada_x -= 8
        posicao_passada_x = abs(posicao_passada_x)
        posicao_passada_y = ultimo_lance[3]
        posicoes_y_possiveis = {"0":"A", "1":"B", "2":"C", "3":"D", "4":"E", "5":"F", "6":"G", "7":"H"}
        posicao_passada_y = posicoes_y_possiveis.get(posicao_passada_y)
        posicao_passada = str(posicao_passada_y) + str(posicao_passada_x)

        # Armazena
        jogada += posicao_passada

        # Visualiza a posição
        posicao_futura_x = int(ultimo_lance[4])
        posicao_futura_x -= 8
        posicao_futura_x = abs(posicao_futura_x)
        posicao_futura_y = ultimo_lance[5]  
        posicao_futura_y = posicoes_y_possiveis.get(posicao_futura_y)
        posicao_futura = str(posicao_futura_y) + str(posicao_futura_x)

        # Armazena
        jogada += " para " + posicao_futura

        # Visualiza se foi alguma jogada especial. Ex: Captura, Roque, etc.
        try:
            especial = ultimo_lance[6]
        except IndexError:
            ignorar = True
        if ignorar == False:
            if especial == "x":
                jogada += " Xeque "
                xeque = True
                try:
                    especial = ultimo_lance[7]
                except IndexError:
                    pass

            if especial == "R":
                jogada += " Roque grande"
            elif especial == "r":
                jogada += " Roque curto"
            elif especial == "c":
                jogada += " Capturando "
                if xeque == True:
                    peca_comida = ultimo_lance[8]
                else:
                    peca_comida = ultimo_lance[7]
                peca = pecas_possiveis.get(peca_comida)
                if cor == "Branca" or cor == "Branco":
                    if peca == "Rainha" or peca == "Torre":
                        cor_inimiga = "Preta"
                    else:
                        cor_inimiga = "Preto"
                else:
                    if peca == "Rainha" or peca == "Torre":
                        cor_inimiga = "Branca"
                    else:
                        cor_inimiga = "Branco"
                jogada += peca + " " + cor_inimiga
            elif especial == "e":
                jogada += " En passant"
            elif especial == "p":
                if xeque == True:
                    peca_promovida = ultimo_lance[8]
                else:
                    peca_promovida = ultimo_lance[7]
                peca = pecas_possiveis.get(peca_promovida)
                jogada = "Peão promovido em " + posicao_passada + " para " + peca

        # Atualiza o QLabel
        self.contador_ultimo_lance.setText(jogada)

    def criar_painel_capturas(self):
        """
        Método responsável por criar o painel de captura, exibindo as peças fora de jogo.

        Return:
            painel_captura (QVBoxLayout): painel devidamente preenchido com os ícones e contadores.
        """

        self.painel_captura = QVBoxLayout()
        self.painel_captura.setSpacing(5)
        self.painel_captura.setContentsMargins(0, 10, 0, 10)

        self.labels_capturas = {}

        # Definição das peças brancas
        pecas_brancas = ["pawn_white_chibi.png", "rook_white_chibi.png", "horse_white_chibi.png",
                        "bishop_white_chibi.png", "queen_white_chibi.png"]

        # Definição das peças pretas
        pecas_pretas = ["pawn_black_chibi.png", "rook_black_chibi.png", "horse_black_chibi.png",
                        "bishop_black_chibi.png", "queen_black_chibi.png"]

        def criar_linha(pecas):
            """
            Cria uma linha com ícones e contadores para as peças capturadas.

            Args:
                pecas (list): Lista com os nomes dos arquivos das peças.

            Return:
                linha (QHBoxLayout): Linha com os elementos visuais das capturas.
            """

            linha = QHBoxLayout()
            linha.setSpacing(5)

            for peca in pecas:
                item_layout = QVBoxLayout()
                item_layout.setSpacing(0)
                item_layout.setAlignment(Qt.AlignCenter)

                # Adiciona o ícone da peça
                icone_label = QLabel()
                icone_pixmap = QPixmap(os.path.join(caminho_assets, peca)).scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                icone_label.setPixmap(icone_pixmap)

                # Adiciona os contadores as devidas peças
                contador_label = QLabel(" x 0")
                contador_label.setStyleSheet("color: #EEE8D5; font-size: 16px; font-weight: bold;")
                contador_label.setAlignment(Qt.AlignCenter)
                self.labels_capturas[peca] = contador_label

                item_layout.addWidget(icone_label)
                item_layout.addWidget(contador_label)
                linha.addLayout(item_layout)

            return linha

        header_brancas = QHBoxLayout()
        header_brancas.setAlignment(Qt.AlignCenter)
        header_brancas.setSpacing(4)

        # Adiciona a coroa dos pretos
        crown_black = QLabel()
        crown_pixmap_black = QPixmap(os.path.join(caminho_assets, "crown_black.png")).scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        crown_black.setPixmap(crown_pixmap_black)

        texto_branco = QLabel("CAPTURAS PRETAS:")
        texto_branco.setStyleSheet("color: #EEE8D5; font-size: 16px; font-weight: bold;")

        header_brancas.addWidget(crown_black)
        header_brancas.addWidget(texto_branco)

        self.painel_captura.addLayout(header_brancas)
        self.painel_captura.addLayout(criar_linha(pecas_brancas))

        header_pretas = QHBoxLayout()
        header_pretas.setAlignment(Qt.AlignCenter)
        header_pretas.setSpacing(4)

        # Adiciona a coroa das brancas
        crown_white = QLabel()
        crown_pixmap_white = QPixmap(os.path.join(caminho_assets, "crown_white.png")).scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        crown_white.setPixmap(crown_pixmap_white)

        texto_preto = QLabel("CAPTURAS BRANCAS:")
        texto_preto.setStyleSheet("color: #EEE8D5; font-size: 16px; font-weight: bold;")

        header_pretas.addWidget(crown_white)
        header_pretas.addWidget(texto_preto)

        self.painel_captura.addLayout(header_pretas)
        self.painel_captura.addLayout(criar_linha(pecas_pretas))

        return self.painel_captura
        
    def atualizar_painel_capturas(self):
        """
        Atualiza devidamente os contadores do painel de capturas, com o
        número respectivo de peças já capturadas de cada tipo pro dois lados.
        """
        
        contagem = {
            "pawn_white_chibi.png": self.jogo.lista_pecas_perdidas_brancas.count("P0"),
            "rook_white_chibi.png": self.jogo.lista_pecas_perdidas_brancas.count("R0"),
            "horse_white_chibi.png": self.jogo.lista_pecas_perdidas_brancas.count("H0"),
            "bishop_white_chibi.png": self.jogo.lista_pecas_perdidas_brancas.count("B0"),
            "queen_white_chibi.png": self.jogo.lista_pecas_perdidas_brancas.count("Q0"),
            "pawn_black_chibi.png": self.jogo.lista_pecas_perdidas_pretas.count("P1"),
            "rook_black_chibi.png": self.jogo.lista_pecas_perdidas_pretas.count("R1"),
            "horse_black_chibi.png": self.jogo.lista_pecas_perdidas_pretas.count("H1"),
            "bishop_black_chibi.png": self.jogo.lista_pecas_perdidas_pretas.count("B1"),
            "queen_black_chibi.png": self.jogo.lista_pecas_perdidas_pretas.count("Q1"),
        }
        for peca, label in self.labels_capturas.items():
            qtd = contagem.get(peca, 0)
            label.setText(f" x {qtd}")
        
    def criar_tabuleiro(self):
        """
        Cria os tiles do tabuleiro e adiciona os sinais de clique em cada casa.
        """

        for i in range(8):
            for j in range(8):
                posicao = str(i) + str(j)

                label = CasaLabel(posicao)
                label.setFixedSize(TAMANHO_CASA, TAMANHO_CASA)
                label.clicado.connect(lambda pos = posicao: self.on_casa_clicada(pos))

                cor = "#EEE8D5" if (i + j) % 2 == 0 else "#586E57"

                label.setStyleSheet(f"background-color: {cor};")
                label.setAlignment(Qt.AlignCenter)
                self.grid.addWidget(label, i, j)

                self.casas[posicao] = label


    def adicionar_peca(self, posicao, caminho_imagem, selecionada = False):
        """
        Adiciona uma certa peça em uma certa posição.

        Args:
            posicao (str): Posição onde a peça será adicionada.
            caminho_imagem (str): Caminho da imagem da peça.
            selecionada (bool): Indica se a peça está selecionada.
        """

        if posicao in self.casas:
            label = self.casas[posicao]

            if selecionada == True:
                if "_selected" not in caminho_imagem and "_targeted" not in caminho_imagem:
                    caminho_imagem = caminho_imagem.replace(".png", "_selected.png")
            
            pixmap = QPixmap(caminho_imagem)
            pixmap = pixmap.scaled(TAMANHO_CASA, TAMANHO_CASA, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            label.setPixmap(pixmap)
            label.caminho_imagem = caminho_imagem
    

    def desenhar_tabuleiro(self):
        """
        Atualiza o tabuleiro gráfico, limpando e redesenhando as peças.
        """

        grid = self.jogo.tabuleiro.grid

        for label in self.casas.values():
            label.clear()
            label.setPixmap(QPixmap())
            if hasattr(label, "caminho_imagem"):
                del label.caminho_imagem

        for i in range(8):
            for j in range(8):
                peca = grid[i][j]
                if peca != None:
                    nome = type(peca).__name__.lower()
                    cor = "white" if peca.cor == 0 else "black"
                    nome_arquivo = str(nome) + "_" + str(cor) + ".png"

                    caminho = os.path.join(os.path.dirname(__file__), "..", "assets", nome_arquivo)
                    caminho = os.path.abspath(caminho)
                    posicao = str(i) + str(j)

                    self.adicionar_peca(posicao, caminho)
        self.atualizar_ultimo_lance()
        self.atualizar_painel_capturas()
        
    def selecionar_peca(self, posicao):
        """
        Seleciona uma peça, e permite o jogador movimentar ela dentro do tabuleiro.
        Se já estiver selecionada o jogador pode mover ela até essa posição.

        Args:
            posicao (str): Posição da peça selecionada, ou para onde ela deve se mover.
        """

        if self.promocao_em_andamento:
            return
        
        if self.jogo_finalizado == 1:
            return

        self.limpar_destacado()
        self.indicador_rei_xeque()

        label = self.casas[posicao]

        # Verificando se é uma posição válida.
        if not hasattr(label, "caminho_imagem"):
            if self.ultima_peca_selecionada:
                peca = self.jogo.tabuleiro.get_peca(self.ultima_peca_selecionada)
                if peca.cor != self.cor_jogador:
                    self.ultima_peca_selecionada = 0
                    return
                self.posicao_ultima_jogada_a_limpar.append(posicao)
                self.mover_peca(posicao)
            return
        
        # Verificando se é uma posição válida.
        if self.ultima_peca_selecionada:
            peca_teste = self.jogo.tabuleiro.get_peca(posicao)
            peca_origem = self.jogo.tabuleiro.get_peca(self.ultima_peca_selecionada)
            if peca_origem.cor != peca_teste.cor:
                self.posicao_ultima_jogada_a_limpar.append(posicao)
                self.mover_peca(posicao)
                return
        
        # Caso seja uma seleção e não uma jogada.
        self.ultima_peca_selecionada = posicao
        caminho_original = label.caminho_imagem
        cor = self.casas[posicao].styleSheet()
        self.posicoes_a_limpar.append({"tipo": "peca_selecionada",
                                        "posicao": posicao,
                                        "cor": cor,
                                        "caminho": caminho_original})
        self.adicionar_peca(posicao, caminho_original, selecionada = True)
        self.destacar_movimento(posicao)
        if len(self.posicao_ultima_jogada_a_limpar) > 0:
            self.posicao_ultima_jogada_a_limpar.clear()
        self.posicao_ultima_jogada_a_limpar.append(posicao)

    def on_casa_clicada(self, posicao):
        """
        Trata o clique em uma casa do tabuleiro.

        Args:
            posicao (str): Posição que foi clicado.
        """

        if self.cor_atual != self.cor_jogador or self.promocao_em_andamento:
            return
        self.selecionar_peca(posicao)

    def destacar_movimento(self, posicao):
        """
        Destaca os movimentos possíveis de uma peça ao ser clicada.

        Args:
            posicao (str): Posição da peça no tabuleiro (ex: "23").
        """

        movimentos = self.jogo.calcular_movimento_jogo(posicao, self.cor_atual)

        for i in movimentos:
            if i in self.casas:

                # Mudando a cor da casa
                cor = self.casas[i].styleSheet()
                nova_cor = "#D3CDBB" if cor == "background-color: #EEE8D5;" else "#4B5E4A"
                self.casas[i].setStyleSheet(f"background-color: {nova_cor};")
                
                peca = self.jogo.tabuleiro.get_peca(i)

                # Se a casa estiver vazia, é colocado um ponto
                if peca == None:
                    ponto = QLabel(self.casas[i])
                    caminho = os.path.join(os.path.dirname(__file__), "..", "assets", "dot.png")
                    caminho = os.path.abspath(caminho)
                    ponto.setPixmap(QPixmap(caminho).scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                    ponto.setAlignment(Qt.AlignCenter)
                    ponto.setAttribute(Qt.WA_TransparentForMouseEvents)
                    ponto.setGeometry(0, 0, TAMANHO_CASA, TAMANHO_CASA)
                    self.posicoes_a_limpar.append({"tipo": "movimento_valido",
                                                   'posicao': i,
                                                   'cor': cor,
                                                   'ponto': ponto})
                    ponto.show()
                
                # Caso não esteja, e há um inimigo nela, ele é marcado
                else:
                    label = self.casas[i]
                    nome = type(peca).__name__.lower()
                    cor_peca = "white" if peca.cor == 0 else "black"
                    nome_arquivo = f"{nome}_{cor_peca}_targeted.png"
                    caminho_original = label.caminho_imagem
                    caminho = os.path.join(os.path.dirname(__file__), "..", "assets", nome_arquivo)
                    caminho = os.path.abspath(caminho)
                    self.adicionar_peca(i, caminho)
                    self.posicoes_a_limpar.append({"tipo": "inimigo",
                                                   'posicao': i,
                                                   'cor': cor,
                                                   'caminho': caminho_original})        

    def destacar_jogada(self, jogada_ia = False, posicao = None):
        """
        Destaca a última jogada realizada na partida.

        Args:
            jogada_ia (bool): Flag para identificar se a jogada foi realizada pelo jogador ou o computador.
            posicao (str): String contendo as duas posições, de origem e destino concatenadas (ex: "2434")
        """

        # Se a jogada foi realizada pelo jogador é possível obter através da self.posicao_ultima_jogada_a_limpar
        if jogada_ia == False:
            origem = self.posicao_ultima_jogada_a_limpar[0]
            destino = self.posicao_ultima_jogada_a_limpar[1]
            if origem in self.casas and destino in self.casas:
                cor = self.casas[origem].styleSheet()
                self.casas[origem].setStyleSheet("background-color: rgba(218, 165, 32, 60);")
                self.ultima_jogada_a_limpar.append({"tipo": "jogada",
                                                    "posicao": origem,
                                                    "cor": cor})
                cor = self.casas[destino].styleSheet()
                self.casas[destino].setStyleSheet("background-color: rgba(32, 178, 170, 60);")
                self.ultima_jogada_a_limpar.append({"tipo": "jogada",
                                                    "posicao": destino,
                                                    "cor": cor})
            self.posicao_ultima_jogada_a_limpar.clear()

        # Caso a jogada seja feita pelo computador é preciso passar a posição como parâmetro
        else:
            origem = posicao[:2]
            destino = posicao[2:]
            if origem in self.casas and destino in self.casas:
                cor = self.casas[origem].styleSheet()
                self.casas[origem].setStyleSheet("background-color: rgba(218, 165, 32, 60);")
                self.ultima_jogada_a_limpar.append({"tipo": "jogada",
                                                    "posicao": origem,
                                                    "cor": cor})
                cor = self.casas[destino].styleSheet()
                self.casas[destino].setStyleSheet("background-color: rgba(32, 178, 170, 60);")
                self.ultima_jogada_a_limpar.append({"tipo": "jogada",
                                                    "posicao": destino,
                                                    "cor": cor})
                
    def limpar_destacado(self):
        """
        Limpa os destaques visuais de movimentos válidos ou ataques, restaurando o estado anterior das casas.
        """

        # Procura pelo estados armazenados na lista de posições a limpar
        for i in self.posicoes_a_limpar:
            tipo = i["tipo"]
            posicao = i["posicao"]

            if tipo == "peca_selecionada":
                self.adicionar_peca(posicao, i["caminho"], selecionada=False)

            elif tipo == "movimento_valido":
                self.casas[posicao].setStyleSheet(i["cor"])
                ponto = i.get("ponto")
                ponto.setParent(None)
                ponto.deleteLater() 

            elif tipo == "inimigo":
                self.casas[posicao].setStyleSheet(i["cor"])
                self.adicionar_peca(posicao, i["caminho"])

            elif tipo == "xeque":
                self.adicionar_peca(posicao, i["caminho"])

        self.posicoes_a_limpar.clear()
        return
    
    def limpar_jogada(self):
        """
        Limpa os destaques visuais da última jogada (como cores de origem e destino).
        """
    
        # Restaura a antiga cor
        for i in self.ultima_jogada_a_limpar:
            tipo = i["tipo"]
            posicao = i["posicao"]
            if tipo == "jogada":
                self.casas[posicao].setStyleSheet(i["cor"])
        self.ultima_jogada_a_limpar.clear()
        return        
    
    def mover_peca(self, posicao):
        """
        Move a peça da posição selecionada para a nova posição, se for uma jogada válida.

        Args:
            posicao (str): Posição de destino no tabuleiro.
        """

        origem = self.ultima_peca_selecionada

        # Verificando se é uma jogada válida
        movimentos = self.jogo.calcular_movimento_jogo(origem, self.cor_atual)
        if posicao in movimentos:

            # Aplicando a jogada
            if self.jogo.mover_peca_jogo(origem, posicao) == True:
                self.limpar_jogada()
                self.jogo.verificar_material_fora_de_campo()
                self.desenhar_tabuleiro()
                self.repaint()
                QApplication.processEvents()
                self.destacar_jogada()
                if self.jogo.verificar_promocao_peao():
                    self.exibir_promocao()
                    self.ultima_peca_selecionada = 0
                    return
                self.cor_atual = 1 - self.cor_atual

        self.ultima_peca_selecionada = 0
        self.indicador_rei_xeque()

        # Verificando empate
        self.empate_por_material_insuficiente = self.jogo.verificar_insuficiencia_de_material()
        if self.empate_por_material_insuficiente == "EMPATE":
            self.mostrar_fim_de_jogo("Empate por material insuficiente!")
            return
        
        # Verificando possível Xeque-Mate
        self.jogo_finalizado = self.jogo.verificar_xeque_mate(self.cor_atual)
        if self.jogo_finalizado == 1:
            self.mostrar_fim_de_jogo("Xeque-Mate! Pretas venceram.")
            return
        if self.jogo_finalizado == 2:
            self.mostrar_fim_de_jogo("Xeque-Mate! Brancas venceram.")
            return
        if self.jogo_finalizado == 3:
            self.mostrar_fim_de_jogo("Empate por afogamento.")
            return
        if self.cor_atual != self.cor_jogador:
            QTimer.singleShot(200, self.jogar_ia)
            self.jogo_finalizado = self.jogo.verificar_xeque_mate(self.cor_atual)
            if self.jogo_finalizado == 1:
                self.mostrar_fim_de_jogo("Xeque-Mate! Pretas venceram.")
                return
            if self.jogo_finalizado == 2:
                self.mostrar_fim_de_jogo("Xeque-Mate! Brancas venceram.")
                return
            if self.jogo_finalizado == 3:
                self.mostrar_fim_de_jogo("Empate por afogamento.")
                return
            
    def exibir_promocao(self):
        """
        Responsável por exibir a tela de promoções assim que um peão chegar no fim do tabuleiro.
        """

        self.promocao_em_andamento = 1
        cor = self.cor_atual

        self.menu_promocao = PromocaoWidget(cor)
        self.menu_promocao.peca_escolhida.connect(self.promover_peao)

        # Configurando no meio da tela
        geometria = self.geometry()
        dialog_geometria = self.menu_promocao.frameGeometry()
        center_x = geometria.center().x() - dialog_geometria.width() // 2
        center_y = geometria.center().y() - dialog_geometria.height() // 2
        self.menu_promocao.move(center_x, center_y) 
        self.menu_promocao.exec_()  

    def promover_peao(self, peca_str):
        """
        Promove o peão, trocando ele pela peça escolhido pelo jogador.

        Args:
            peca_str (str): Nome da peça escolhida.
        """

        self.jogo.promover_peao(peca_str)
        self.desenhar_tabuleiro()
        self.promocao_em_andamento = 0
        self.cor_atual = 1 - self.cor_atual
        self.jogo.verificar_xeque_mate(self.cor_atual)
        self.indicador_rei_xeque()
        if self.cor_atual != self.cor_jogador:
            QTimer.singleShot(200, self.jogar_ia)

    def salvar_partida(self):
        """
        Abre uma janela para salvar o estado atual da partida em um arquivo .json.
        """

        if self.ultima_peca_selecionada:
            return

        caminho_arquivo, _ = QFileDialog.getSaveFileName(
            self,
            "Salvar Partida",
            "./save/partida.json",
            "Arquivos JSON (*.json)"
        )

        if caminho_arquivo:
            self.jogo.salvar_partida(caminho_arquivo)

    def verificar_xeque(self):
        """
        Verifica possíveis xeques.
        """

        # Zera os atributos
        self.rei_branco_xeque = 0
        self.rei_preto_xeque = 0

        # Vaculha o tabuleiro em busca das peças
        for i in range(8):
            for j in range(8):
                pos = f"{i}{j}"
                peca = self.jogo.tabuleiro.get_peca(pos)

                # Se de fato for uma peça procura os movimentos delas
                if peca:
                    peca.movimento(self.jogo.tabuleiro.grid)
                    moveset = peca.lista_posicoes_validas

                    # Caso seja uma peça branca
                    if peca.cor == 0:
                        for m in moveset:
                            if m == self.jogo.posicao_rei_preto:
                                self.rei_preto_xeque = 1

                    # Caso seja uma peça preta
                    if peca.cor == 1:
                        for m in moveset:
                            if m == self.jogo.posicao_rei_branco:
                                self.rei_branco_xeque = 1

    def indicador_rei_xeque(self):
        """
        Atualiza o visual do tabuleiro para destacar o rei que está em xeque.
        """

        self.verificar_xeque()
        self.posicoes_a_limpar = [i for i in self.posicoes_a_limpar if i["tipo"] != "xeque"]
        for i in range(8):
            for j in range(8):
                
                pos = str(i) + str(j)
                peca = self.jogo.tabuleiro.get_peca(pos)

                if peca and type(peca).__name__.lower() == "king":
                    if pos in self.casas:   
                        label = self.casas[pos]

                        if hasattr(label, "caminho_imagem") and "_targeted" in label.caminho_imagem:
                            nome = type(peca).__name__.lower()
                            cor_peca = "white" if peca.cor == 0 else "black"
                            nome_arquivo = f"{nome}_{cor_peca}.png"
                            caminho = os.path.join(os.path.dirname(__file__), "..", "assets", nome_arquivo)
                            caminho = os.path.abspath(caminho)
                            self.adicionar_peca(pos, caminho)

        if self.rei_branco_xeque == 1:
            posicao = self.jogo.posicao_rei_branco
            peca = self.jogo.tabuleiro.get_peca(posicao)
        elif self.rei_preto_xeque == 1:
            posicao = self.jogo.posicao_rei_preto
            peca = self.jogo.tabuleiro.get_peca(posicao)
        else:
            return  
        
        label = self.casas[posicao]
        nome = type(peca).__name__.lower()
        cor_peca = "white" if peca.cor == 0 else "black"
        nome_arquivo = f"{nome}_{cor_peca}_targeted.png"
        caminho_original = label.caminho_imagem
        caminho = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", nome_arquivo))
        self.adicionar_peca(posicao, caminho)
        self.posicoes_a_limpar.append({"tipo": "xeque", 'posicao': posicao, 'caminho': caminho_original})
            
    def voltar_jogada(self):
        """
        Desfaz a última jogada executada.
        """

        if self.ultima_peca_selecionada:
            return

        self.limpar_jogada()
        self.jogo.voltar_jogada()
        self.desenhar_tabuleiro()
        self.cor_atual = 1 - self.cor_atual 
        
        if self.jogo.verificar_promocao_peao() == True:
            self.exibir_promocao()

    def jogar_ia(self):
        """
        Executa a jogada da IA, atualizando o tabuleiro e verificando condições de fim de jogo.
        """

        # A IA escolha a sua ação
        posicoes = self.jogo.jogar_ia()

        self.limpar_jogada() 
        self.jogo.verificar_material_fora_de_campo()
        self.destacar_jogada(jogada_ia = True, posicao = posicoes)
        
        self.desenhar_tabuleiro()
        self.repaint()
        QApplication.processEvents()

        self.cor_atual = 1 - self.cor_atual
        self.ultima_peca_selecionada = 0 

        self.indicador_rei_xeque()

        # Verificar possível empate
        self.empate_por_material_insuficiente = self.jogo.verificar_insuficiencia_de_material()
        if self.empate_por_material_insuficiente == "EMPATE":
            self.mostrar_fim_de_jogo("Empate por material insuficiente!")

        # Verificar possível Xeque-Mate
        self.jogo_finalizado = self.jogo.verificar_xeque_mate(self.cor_atual)
        if self.jogo_finalizado == 1:
            self.mostrar_fim_de_jogo("Xeque-Mate! Pretas venceram.")
            return
        if self.jogo_finalizado == 2:
            self.mostrar_fim_de_jogo("Xeque-Mate! Brancas venceram.")
            return
        if self.jogo_finalizado == 3:
            self.mostrar_fim_de_jogo("Empate por afogamento.")
            return
        
        # Verificar possível promoção
        if self.jogo.verificar_promocao_peao():
            peca = self.jogo.tabuleiro.get_peca(self.jogo.promover_posicao)
            if peca.cor != self.cor_jogador:
                self.jogo.colocar_peca_promovida_ia(peca.cor, self.jogo.promover_posicao)
            else: 
                self.exibir_promocao()

    def jogar_ia_vs_ia(self):
        """
        Controla o fluxo do jogo no modo IA vs IA, alternando entre as jogadas das duas IAs.
        """
        cor_atual = self.jogo.turno % 2
        if cor_atual == 0:
            self.ia_atual = self.ia_branca
        else:
            self.ia_atual = self.ia_preta

        self.ia_atual.simular_jogada()
        QTimer.singleShot(300, self.aplicar_jogada_ia)

    def aplicar_jogada_ia(self):
        """
        Aplica a jogada escolhida pela IA, verifica promoções, xeque-mate, empates
        e atualiza visualmente o tabuleiro.
        """

        # Aplica a jogada
        self.ia_atual.aplicar_jogada_escolhida()
        movimento = self.ia_atual.avaliar_movimento()
        if movimento:
            origem = movimento[:2]
            destino = movimento[2:]
            self.jogo.mover_peca_jogo(origem, destino)
            posicoes = f"{origem}{destino}"

            self.limpar_jogada()
            self.jogo.verificar_material_fora_de_campo()
            self.destacar_jogada(jogada_ia = True, posicao = posicoes)

        # Se for possível promover, promove
        if self.jogo.verificar_promocao_peao():
            peca = self.jogo.tabuleiro.get_peca(self.jogo.promover_posicao)
            self.jogo.colocar_peca_promovida_ia(peca.cor, self.jogo.promover_posicao)

        self.desenhar_tabuleiro()
        self.repaint()
        QApplication.processEvents()

        self.cor_atual = 1 - self.cor_atual
        self.indicador_rei_xeque()

        # Verifica algum possível empate
        if self.jogo.verificar_insuficiencia_de_material() == "EMPATE":
            self.reiniciar()
            QTimer.singleShot(700, self.jogar_ia_vs_ia)
            return

        # Verifica xeque-mate e empate por afogamento
        resultado = self.jogo.verificar_xeque_mate(self.cor_atual)
        if resultado in (1, 2, 3):
            self.reiniciar()
            QTimer.singleShot(700, self.jogar_ia_vs_ia)
            return

        QTimer.singleShot(700, self.jogar_ia_vs_ia)

    def reiniciar(self):
        """
        Reinicia o jogo, zerando o tabuleiro e os estados internos.
        """

        if self.ultima_peca_selecionada:
            return

        self.limpar_jogada()
        self.limpar_destacado()
        self.jogo.reiniciar()
        self.jogo_finalizado = 0
        self.desenhar_tabuleiro()
        self.repaint()
        QApplication.processEvents()
        if self.cor_jogador == 1:
            self.jogar_ia()

    def mostrar_fim_de_jogo(self, mensagem):
        """
        Chama a tela de fim de jogo.
        """

        self.close()

        self.tela_fim = TelaFimDeJogo(
            mensagem_fim = mensagem, 
            interface_original = MainWindow,
        )
        self.tela_fim.show()

def iniciar_interface():
    """
    Inicializa e exibe a interface gráfica principal do jogo.
    """

    app = QApplication(sys.argv)
    janela = MainWindow(modo_ia_vs_ia = True) 
    janela.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    iniciar_interface()