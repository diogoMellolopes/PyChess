class Board:
    """
    Classe Board.

    Represente o tabuleiro do jogo de Xadrez.

    Responsável por gerenciar o estado do jogo, atualizar as posições
    das peças e controlar movimentos válidos no tabuleiro.
    """

    def __init__(self):
        """
        Inicializa o tabuleiro como uma matriz 8x8 preenchida com "None".
        """

        self.grid = [[None for _ in range (8)] for _ in range(8)]

    def posiciona_peca(self, peca, posicao):
        """
        Posiciona uma determinada peça em uma posição específica (Ex: "04").

        Args:
            peca (object | None): Instância da peça a ser posicionada, ou None se for remover.
            posicao (str): Posição concatenada de dois números, onde o primeiro representa o x e o segundo o y.
        """

        # Pegando as posições de x e y
        x, y = int(posicao[0]), int(posicao[1])
        self.grid[x][y] = peca

    def get_peca(self, posicao):
        """
        Retorna a peça que está armazenada em uma determinada posição.

        Args:
            posicao (str): Posição no formato "xy".

        Returns:
            Object | None: Instância da peça, ou None se a casa estiver vazia.
        """

        x, y = int(posicao[0]), int(posicao[1])
        return self.grid[x][y]
    
    def mover_peca(self, origem, destino, roque_preto = False, roque_branco = False, en_passant = False):
        """
        Move uma peça de "origem" até "destino", aplicando regras especiais (roque, en passant).

        Args:
            origem (str): posição de origem dessa peça. (Ex: "04").
            destino (str): posição final dessa peça. (Ex: "05").
            roque_preto (bool): Se True, indica roque das pretas.
            roque_branco (bool): Se True, indica roque das brancas.
            en_passant (bool): Se True, indica movimento en passant.

        Returns:
            bool: True se a jogada foi executada com sucesso, False caso contrário.
        """

        # Pega a posição, e a sua determinada peça
        x, y = int(destino[0]), int(destino[1])
        peca = self.get_peca(origem)

        # Se for roque branco, verifica a posição de destino
        if roque_branco == True:
            self.posiciona_peca(peca, destino)
            self.posiciona_peca(None, origem)
            peca.posicao = destino

            # Será um roque curto
            if destino == "76":
                torre = self.get_peca("77")
                self.posiciona_peca(torre, "75")
                self.posiciona_peca(None, "77")
                torre.posicao = "75"
                torre.mexeu += 1
                return True
            
            # Será um roque longo
            if destino == "72":
                torre = self.get_peca("70")
                self.posiciona_peca(torre, "73")
                self.posiciona_peca(None, "70")
                torre.posicao = "73"
                torre.mexeu += 1
                return True
            
        # Se for roque preto, verifica a posição de destino
        if roque_preto == True:
            self.posiciona_peca(peca, destino)
            self.posiciona_peca(None, origem)
            peca.posicao = destino

            # Será um roque curto
            if destino == "06":
                torre = self.get_peca("07")
                self.posiciona_peca(torre, "05")
                self.posiciona_peca(None, "07")
                torre.posicao = "05"
                torre.mexeu += 1
                return True
            
            # Será um roque longo
            if destino == "02":
                torre = self.get_peca("00")
                self.posiciona_peca(torre, "03")
                self.posiciona_peca(None, "00")
                torre.posicao = "03"
                torre.mexeu += 1
                return True
            
        # Se for um en passant, calcula a posição do peão comido, e subtitui por None
        if en_passant == True:
            direcao = 1 if peca.cor == 0 else -1
            linha = int(destino[0])
            coluna = int(destino[1])
            posicao_antigo_peao = str(linha + direcao) + str(coluna)
            self.posiciona_peca(None, posicao_antigo_peao)
            self.posiciona_peca(peca, destino)
            self.posiciona_peca(None, origem)
            peca.posicao = destino
            return True
            
        # Coloca a peça na posição de destino, e o none na posição antiga da peça
        self.posiciona_peca(peca, destino)
        self.posiciona_peca(None, origem)
        peca.posicao = destino

        # Caso tenha ocorrido como esperado, retorna True
        if self.grid[x][y] != None:
            return True
        else:
            return False

    def printar_tabuleiro(self):
        """
        Exibe o tabuleiro no console em formato legível.

        Cada casa mostra:
            - A letra inicial da peça.
            - A cor: "b" para branco, "p" para preto.
            - "--" para casas vazias.
        """

        cont = 0
        print("%  0   1   2   3   4   5   6   7")
        for x in range(8):
            linha = str(cont) + " "
            for y in range(8):
                if self.grid[x][y] != None:
                    peca = self.grid[x][y]
                    letra = type(peca).__name__[0]
                    cor = 'b' if peca.cor == 0 else 'p'
                    linha += " " + letra + cor + " "
                else:
                    linha += " -- "
            print(linha)
            cont += 1

    def calcular_movimento(self, posicao):
        """
        Calcula os movimentos válidos para a peça em determinada posição.

        Args:
            posicao (str): Posição da peça a ter seus movimentos calculados. No formato "xy".

        Returns:
            list[str] | str: Lista de movimentos válidos. Retorna "99" se não houver peça.
        """

        # Pega a peça
        peca = self.get_peca(posicao)
        if peca == None:
            return "99"
        
        # Calcula os seus movimentos
        peca.movimento(self.grid)

        # Armazena no moveset
        moveset = peca.lista_posicoes_validas
        return moveset
    
    def reiniciar(self):
        """
        Reinicia o tabuleiro para o estado inicial (matriz 8x8 com `None`).
        """

        self.grid = [[None for _ in range (8)] for _ in range(8)]