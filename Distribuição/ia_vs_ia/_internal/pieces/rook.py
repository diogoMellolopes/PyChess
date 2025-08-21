from .piece import Piece # import da classe pai Piece

class Rook(Piece):
    """
    Classe Torre, herdando a classe pai Piece.

    Representa o comportamento de uma torre no Xadrez, incluindo o seu movimento em reta.

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
        Método que calcula os movimentos básicos da Torre, baseado na posição atual e no estado do tabuleiro.

        A Torre avança e captura nas suas quatro retas adjacentes (horizontal e vertical).
        """

        self.lista_posicoes_validas.clear()

        x = int(self.posicao[0])
        y = int(self.posicao[1])

        # Direcoes das retas: (dx, dy)
        direcoes = [ (1, 0), (-1, 0), (0, 1), (0, -1) ]

        # Calculo do movimento reto da Torre
        for dx, dy in direcoes:
            for i in range(1, 8):
                novo_x = x + dx * i
                novo_y = y + dy * i

                if not (0 <= novo_x <= 7 and 0 <= novo_y <= 7):
                    break

                peca = tabuleiro[novo_x][novo_y]
                destino = f"{novo_x}{novo_y}"

                if peca == None:
                    self.lista_posicoes_validas.append(destino)
                else:
                    if peca.cor != self.cor:
                        self.lista_posicoes_validas.append(destino)
                    break 

        return