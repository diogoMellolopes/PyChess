from .piece import Piece # Import da classe pai Piece

class King(Piece):
    """
    Classe Rei, herdando a classe pai Piece.

    Representa o comportamento de um Rei no Xadrez, incluido seu movimento uma casa em todas as direções adjacentes.

    Atributos:
        cor (int): Cor da peça (0 para branco, 1 para preto).
        posicao (str): Posição atual da peça no tabuleiro, ex: "04" (linha 0, coluna 4).
        lista_posicoes_validas (list): Lista de posições válidas que essa peça pode se mover, ex: ["02", "03", "04"].
        mexeu (int): Flag que indica se a peça já se moveu (0 = não, 1 = sim).
    """

    def __init__(self, cor, posicao, lista_posicoes_validas = None):
        # Chamada ao construtor da classe base
        if lista_posicoes_validas is None:
            lista_posicoes_validas = []
        super().__init__(cor, posicao, lista_posicoes_validas)
        self.mexeu = 0

    def movimento(self, tabuleiro):
        """
        Método que calcula os movimentos básicos do Rei no Xadrez, baseado na posição atual e no estado do tabuleiro.

        O Rei move-se uma casa em qualquer direção (horizontal, vertical ou diagonal).
        """

        self.lista_posicoes_validas.clear()

        x = int(self.posicao[0])
        y = int(self.posicao[1])
        
        # Calculo do movimento do Rei
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue

                novo_x = x + j
                novo_y = y + i

                if 0 <= novo_y <= 7 and 0 <= novo_x <= 7:
                    destino = f"{novo_x}{novo_y}"
                    peca = tabuleiro[novo_x][novo_y]
                    if peca == None or peca.cor != self.cor:
                        self.lista_posicoes_validas.append(destino)
        
        return 