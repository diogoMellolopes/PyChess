from .piece import Piece # Import da classe pai Piece.

class Pawn(Piece):
    """
    Classe Peão, herdando a classe pai Piece.

    Representa o comportamento do peão no Xadrez, incluindo seu movimento padrão, movimento inicial
    de suas casas e capturas diagonais.

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
        Método que calcula os movimentos do Peão, baseado na posição atual e no estado do tabuleiro.

        O peão pode:
            - Avançar uma casa pra frente se estiver livre.
            - Avançar duas casas pra frente se estiver livre e for o seu primeiro movimento.
            - Capturar peças inimigas nas diagonais à frente.
        """

        self.lista_posicoes_validas.clear()

        x = int(self.posicao[0])
        y = int(self.posicao[1])
        direcao = -1 if self.cor == 0 else 1 #Branco sobe, e preto desce

        # Movimento normal de uma casa para frente
        novo_x = (x + direcao)
        if 0 <= novo_x <= 7:
            if tabuleiro[novo_x][y] == None:
                destino = f"{novo_x}{y}"
                self.lista_posicoes_validas.append(destino)

                # Movimento inicial de duas casas
                if (x == 6 and self.cor == 0) or (x == 1 and self.cor == 1):
                    novo_x = (x + 2 * direcao)
                    if tabuleiro[novo_x][y] == None:
                        destino = f"{novo_x}{y}"
                        self.lista_posicoes_validas.append(destino)
                    novo_x = (x + direcao)

            # Captura à direta
            novo_y = y + 1
            if 0 <= novo_y <= 7:
                if tabuleiro[novo_x][novo_y] != None:
                    peca = tabuleiro[novo_x][novo_y]
                    if peca.cor != self.cor:
                        destino = f"{novo_x}{novo_y}"
                        self.lista_posicoes_validas.append(destino)

            # Captura à esquerda
            novo_y = y - 1
            if 0 <= novo_y <= 7:
                if tabuleiro[novo_x][novo_y] != None:
                    peca = tabuleiro[novo_x][novo_y]
                    if peca.cor != self.cor:
                        destino = f"{novo_x}{novo_y}"
                        self.lista_posicoes_validas.append(destino)

        return