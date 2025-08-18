class Piece:
    """
    Classe pai para todas as peças do Xadrez.

    Atributos:
        cor (int): Cor da peça (0 para branco, 1 para preto).
        posicao (str): Posição atual da peça no tabuleiro, ex: "04" (linha 0, coluna 4).
        lista_posicoes_validas (list): Lista de posições válidas que essa peça pode se mover, ex: ["02", "03", "04"].
    """

    def __init__(self, cor, posicao, lista_posicoes_validas = None):
        """
        Inicializa uma nova peça.

        Args:
            cor (int): Cor da peça (0 para branco, 1 para preto).
            posicao (str): Posição inicial da peça no formato "xy".
            lista_posicoes_validas (list, optional): Lista de posições válidas iniciais. Defaults to [].
        """

        self.cor = cor
        self.posicao = posicao
        self.lista_posicoes_validas = lista_posicoes_validas if lista_posicoes_validas else []
        
    def movimento(self):
        """
        Método que calcula os movimentos válidos da peça a partir de sua posição atual. É sobrescrito nas classes filhas.
        """
        pass
