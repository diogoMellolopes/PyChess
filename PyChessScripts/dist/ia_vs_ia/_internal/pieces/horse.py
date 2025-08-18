from .piece import Piece # Import da classe pai Piece.

class Horse(Piece):
    """
    Classe Cavalo, herdando a classe pai Piece.

    Representa o comportamento do cavalo no Xadrez, incluindo seu movimento em L.

    Atributos:
        cor (int): Cor da peça (0 para branco, 1 para preto).
        posicao (str): Posição atual da peça no tabuleiro, ex: "04" (linha 0, coluna 4).
        lista_posicoes_validas (list): Lista de posições válidas que essa peça pode se mover, ex: ["02", "03", "04"].
    """

    def __init__(self, cor, posicao, lista_posicoes_validas = None):
        # Chamada ao construtor da classe base
        if lista_posicoes_validas is None:
            lista_posicoes_validas = []
        super().__init__(cor, posicao, lista_posicoes_validas)

    def movimento(self, tabuleiro):
        """
        Método que calcula os movimentos básicos do Cavalo, baseado na posição atual e no estado do tabuleiro.

        O Cavalo pode:
            - Avançar e capturar em L na vertical.
            - Avançar e capturar em L na horizontal.
        """

        self.lista_posicoes_validas.clear()

        x = int(self.posicao[0])
        y = int(self.posicao[1])

        # Lista de movimentos X e Y do cavalo
        movimentos = [
            (1, 2), (1, -2), (-1, 2), (-1, -2),
            (2, 1), (2, -1), (-2, 1), (-2, -1)
        ]

        # Calculo da posições possíveis do cavalo se mover
        for mx, my in movimentos:
            novo_x = x + mx
            novo_y = y + my
            if 0 <= novo_x <= 7 and 0 <= novo_y <= 7:
                peca = tabuleiro[novo_x][novo_y]
                if peca is None or peca.cor != self.cor:
                    destino = f"{novo_x}{novo_y}"
                    self.lista_posicoes_validas.append(destino)

        return 