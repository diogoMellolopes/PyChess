# Imports necessários
from pieces import *
from board import Board
from ia import IA
import json
import os

class Game:
    """
    Classe Game.

    Controlador principal da lógica do jogo de Xadrez.

    Responsável por gerenciar todas as peças, validar jogadas, aplicar as regras
    oficiais do jogo e integrar a IA para simulações e jogadas automáticas.

    Attributes:
        tabuleiro (Board): Instância do tabuleiro principal.
        copia_grid (list[list]): Cópia do tabuleiro para simulações de jogadas.
        posicao_rei_branco (str): Posição atual do rei branco.
        posicao_rei_preto (str): Posição atual do rei preto.
        rei_branco_check (int): Indica se o rei branco está em xeque (1 = sim, 0 = não).
        rei_preto_check (int): Indica se o rei preto está em xeque (1 = sim, 0 = não).
        roque_branco (int): Flag que indica possibilidade de roque das brancas.
        roque_preto (int): Flag que indica possibilidade de roque das pretas.
        en_passant (int): Flag que indica possibilidade de en passant.
        promover_posicao (str): Posição de um peão apto à promoção.
        historico (list): Lista de jogadas executadas.
        turno (int): Contador do turno atual.
        ia (IA): Instância da inteligência artificial associada.
        lista_pecas_perdidas_pretas (list): Peças pretas que foram capturadas.
        lista_pecas_perdidas_brancas (list): Peças brancas que foram capturadas.
    """

    def __init__(self, carregar = False, cor_ia = 1):
        """
        Inicializa a lógica do jogo, juntamente dos seus principais atributos.

        Args:
            carregar (bool, optional): Se True: evita começar o jogo, com as peças nos seus lugares iniciais.
                (usado para carregar partidas salvas). Default é False.
            cor_ia (int, optional): Representa a cor que a IA irá jogar nessa partida. (0 para branco, 1 para preto).
                Default é 1.
        """

        # Inicialização do tabuleiro
        self.tabuleiro = Board()

        # Inicialização dos atributos
        self.copia_grid = [[None for _ in range (8)] for _ in range(8)]
        self.posicao_rei_branco = 0
        self.posicao_rei_preto = 0
        self.posicao_teste_rei_preto = 0
        self.posicao_teste_rei_branco = 0
        self.rei_branco_check = 0
        self.rei_preto_check = 0
        self.roque_branco = 0
        self.roque_preto = 0
        self.en_passant = 0
        self.promover_posicao = 0

        # Inicialização da lista, que representa o histórico
        self.historico = []
        self.turno = 0

        # Inicialização da IA
        self.ia = IA(self, cor_ia)

        # Inicialização da lista, que guarda as peças perdidas de cada lado
        self.lista_pecas_perdidas_pretas = []
        self.lista_pecas_perdidas_brancas = []
        
        # Caso, esteja carregando um jogo, já salvo, evita de inicializar novamente as peças
        if carregar == False:
            self.inicializar_pecas()

    def inicializar_pecas(self):
        """
        Inicializa todas as peças na posição padrão de ínicio do Xadrez.
        """

        # Peões
        for i in range(8):
            y = i
            x = 1
            posicao = str(x) + str(y)
            self.tabuleiro.posiciona_peca(Pawn(1, posicao), posicao)
            x = 6
            posicao = str(x) + str(y)
            self.tabuleiro.posiciona_peca(Pawn(0, posicao), posicao)

        # Torres
        self.tabuleiro.posiciona_peca(Rook(1, "00"), "00")
        self.tabuleiro.posiciona_peca(Rook(1, "07"), "07")
        self.tabuleiro.posiciona_peca(Rook(0, "70"), "70")
        self.tabuleiro.posiciona_peca(Rook(0, "77"), "77")

        # Cavalos
        self.tabuleiro.posiciona_peca(Horse(1, "01"), "01")
        self.tabuleiro.posiciona_peca(Horse(1, "06"), "06")
        self.tabuleiro.posiciona_peca(Horse(0, "71"), "71")
        self.tabuleiro.posiciona_peca(Horse(0, "76"), "76")

        # Bispos
        self.tabuleiro.posiciona_peca(Bishop(1, "02"), "02")
        self.tabuleiro.posiciona_peca(Bishop(1, "05"), "05")
        self.tabuleiro.posiciona_peca(Bishop(0, "72"), "72")
        self.tabuleiro.posiciona_peca(Bishop(0, "75"), "75")

        # Rainhas
        self.tabuleiro.posiciona_peca(Queen(1, "03"), "03")
        self.tabuleiro.posiciona_peca(Queen(0, "73"), "73")

        # Reis
        self.tabuleiro.posiciona_peca(King(1, "04"), "04")
        self.tabuleiro.posiciona_peca(King(0, "74"), "74")

    def posiciona_peca_jogo(self, peca, posicao):
        """
        Posiciona uma determinada peça no tabuleiro simulado (cópia do tabuleiro real).

        Args:
            peca (object | None): Instância da peça a ser posicionada, ou None se for remover.
            posicao (str): Posição concatenada de dois números, onde o primeiro representa o x e o segundo o y. (Ex: "04")
        """

        # Pegando as posições de x e y
        x, y = int(posicao[0]), int(posicao[1])
        self.copia_grid[x][y] = peca

    def get_peca_jogo(self, posicao):
        """
        Obtém a peça de uma posição no tabuleiro simulado.

        Args:
            posicao (str): Posição no formato "xy".

        Returns:
            Object | None: A peça na posição informada, ou None se estiver vazia.
        """

        x, y = int(posicao[0]), int(posicao[1])
        return self.copia_grid[x][y]
    
    def criar_copia_tabuleiro(self):
        """
        Cria uma cópia do tabuleiro real no tabuleiro simulado.

        A cópia é usada para verificar movimentos sem alterar o estado real do jogo.
        Também atualiza as posições atuais dos reis para referência em verificações
        de xeque, roque e xeque-mate.
        """


        for i in range(8):
            for j in range(8):
                self.copia_grid[i][j] = self.tabuleiro.grid[i][j]
                peca = self.copia_grid[i][j]
                if peca:

                    # Atualiza a posição dos reis
                    if type(peca).__name__.lower() == "king" and peca.cor == 0:
                        self.posicao_rei_branco = str(i) + str(j)
                    elif type(peca).__name__.lower() == "king" and peca.cor == 1:
                        self.posicao_rei_preto = str(i) + str(j)

    def verificar_xeque(self):
        """
        Verifica se algum dos reis sofreu um xeque após o último movimento executado.

        Percorre todas as peças no tabuleiro simulado, calcula seus movimentos e identifica se alguma
        delas ameaça a posição atual dos reis. Caso sim, é considerado o Xeque.

        Atualiza:
            rei_branco_check (int): 1 se o rei branco está em xeque, 0 caso contrário.
            rei_preto_check (int): 1 se o rei preto está em xeque, 0 caso contrário.
        """

        # Reseta os atributos
        self.rei_branco_check = 0
        self.rei_preto_check = 0

        # Laço para vasculhar todo o tabuleiro
        for i in range(8):
            for j in range(8):
                peca = self.copia_grid[i][j]
                if peca:

                    # Se algum dos possíveis movimento dessa peça ameaçar o rei, é considerado xeque
                    peca.movimento(self.copia_grid)
                    moveset = peca.lista_posicoes_validas

                    # Caso seja uma peça branca
                    if peca.cor == 0:
                        for m in moveset:
                            if m == self.posicao_teste_rei_preto:

                                # Atualiza o atributo
                                self.rei_preto_check = 1

                    # Caso seja uma peça preta
                    if peca.cor == 1:
                        for m in moveset:
                            if m == self.posicao_teste_rei_branco:

                                # Atualiza o atributo
                                self.rei_branco_check = 1

    def mover_peca_jogo(self, origem, destino):
        """
        Move uma peça no tabuleiro real e atualiza o estado do jogo.
        Considera as regras especias do Xadrez.

        Atualiza:
            - Tabuleiro simulado (cópia).
            - Flags de xeque.
            - Histórico de movimentos.

        Args:
            origem (str): posição de origem dessa peça. (Ex: "04").
            destino (str): posição final dessa peça. (Ex: "05").

        Returns:
            bool: True se a jogada foi executada com sucesso, False caso contrário.
        """

        # Verifica se seria uma possível captura
        peca_destino_antes = self.tabuleiro.get_peca(destino)
        houve_captura = peca_destino_antes is not None
        peca_capturada_letra = type(peca_destino_antes).__name__[0].upper() if houve_captura else ""

        # É pego os outros atributos necessários
        peca = self.tabuleiro.get_peca(origem)
        letra = type(peca).__name__[0].upper()
        cor = "b" if peca.cor == 0 else "p"

        # Caso seja uma torre ou o rei, é necessário contabilizar o atributo "mexeu"
        if type(peca).__name__.lower() in ["king", "rook"]:
            peca.mexeu += 1

            # Se for um roque curto das pretas
            if origem == "74" and destino == "76" and self.roque_branco:

                # Move a peça no tabuleiro original
                self.tabuleiro.mover_peca(origem, destino, roque_branco = True)

                # Atualiza o atributo conforme é preciso
                self.roque_branco = 2

                # Cria uma cópia e verifica se foi uma jogada que resulta em xeque
                self.criar_copia_tabuleiro()
                self.verificar_xeque()

                # Salva o histórico com os atributos necessários
                self.salvar_historico(letra, cor, origem, destino, roque_branco = True, captura = houve_captura, letra_capturada = peca_capturada_letra)
                return True
            
            # Se for um roque longo das pretas
            if origem == "74" and destino == "72" and self.roque_branco:
                self.tabuleiro.mover_peca(origem, destino, roque_branco = True)
                self.roque_branco = 2
                self.criar_copia_tabuleiro()
                self.verificar_xeque()
                self.salvar_historico(letra, cor, origem, destino, roque_branco = True, captura = houve_captura, letra_capturada = peca_capturada_letra)
                return True
            
            # Se for um roque curto das brancas
            if origem == "04" and destino == "06" and self.roque_preto:
                self.tabuleiro.mover_peca(origem, destino, roque_preto = True)
                self.roque_preto = 2
                self.criar_copia_tabuleiro()
                self.verificar_xeque()
                self.salvar_historico(letra, cor, origem, destino, roque_preto = True, captura = houve_captura, letra_capturada = peca_capturada_letra)
                return True
            
            # Se for um roque longo das brancas
            if origem == "04" and destino == "02" and self.roque_preto:
                self.tabuleiro.mover_peca(origem, destino, roque_preto = True)
                self.roque_preto = 2
                self.criar_copia_tabuleiro()
                self.verificar_xeque()
                self.salvar_historico(letra, cor, origem, destino, roque_preto = True, captura = houve_captura, letra_capturada = peca_capturada_letra)
                return True

        # Se for um en passant
        if self.en_passant:
            self.tabuleiro.mover_peca(origem, destino, en_passant = True)
            self.criar_copia_tabuleiro()
            self.verificar_xeque()
            self.salvar_historico(letra, cor, origem, destino, en_passant = True, captura = houve_captura, letra_capturada = peca_capturada_letra)
            return True

        # Caso seja uma jogada comum (captura / movimento)
        self.tabuleiro.mover_peca(origem, destino)
        self.criar_copia_tabuleiro()
        self.verificar_xeque()
        self.salvar_historico(letra, cor, origem, destino, captura = houve_captura, letra_capturada = peca_capturada_letra)
        return True
        
    def calcular_movimento_jogo(self, posicao, cor_jogador):
        """
        Calcula todos os movimentos válidos para a peça em uma posição.

        O cálculo considera movimentos padrões, e jogadas especiais. 
        Além de bloquear movimentos ilegais.

        Args:
            posicao (str): Posição no formato "xy".
            cor_jogador (int): Cor do jogador a ter seu movimento calculado,
            representada por um inteiro. (0 para branco, 1 para preto).

        Returns:
            list[str]: Lista de movimento válidos e filtrados. 
            str: Retorna "99" se não houver uma peça na posição consultada.
        """

        # É armazenado para testar as posições atuais dos reis
        self.posicao_teste_rei_preto = self.posicao_rei_preto
        self.posicao_teste_rei_branco = self.posicao_rei_branco

        movimentos = []

        # Pega a peça
        peca = self.tabuleiro.get_peca(posicao)
        if peca == None:
            return "99"

        # Calcula a lista de seus movimentos
        peca.movimento(self.tabuleiro.grid)

        # Caso seja um rei, é verificado a possibilidade de fazer um roque
        if type(peca).__name__[0].lower() == "k":
            self.verificar_roque(cor_jogador)

        self.verificar_en_passant(posicao)

        moveset = list(peca.lista_posicoes_validas)

        # É analisada individualmente cada possível movimento
        for m in moveset:
            self.criar_copia_tabuleiro()
            destino = m
            origem = peca.posicao

            # Caso seja um rei é necessário atualizar a posição de teste
            if type(peca).__name__[0].lower() == "k":
                if peca.cor == 0:
                    self.posicao_teste_rei_branco = destino
                else:
                    self.posicao_teste_rei_preto = destino
                
            # É colocada a peça nessa nova posição no tabuleiro simulado
            self.posiciona_peca_jogo(peca, destino)
            self.posiciona_peca_jogo(None, origem)

            # Verifica-se o xeque
            self.verificar_xeque()

            # Caso não seja um movimento ilegal é armazenada como válido
            if self.rei_branco_check == 0 and cor_jogador == 0:
                movimentos.append(m)
            if self.rei_preto_check == 0 and cor_jogador == 1:
                movimentos.append(m)
        
        return movimentos
    
    def verificar_xeque_mate(self, cor_jogador):
        """
        Método para verificar possível xeque-mate ou empate por afogamento.

        Análisa todas as peças do jogador e verifica, se há movimentos válidos.
        Se não houver, determina o resultado da partida.

        Args:
            cor_jogador (int): Inteiro que representa a cor do jogador analisado (0 para branco, 1 para preto).
        
        Returns:
            int: 
                0 -> Jogo continua. 
                1 -> Brancas sofreram xeque-mate. (Pretas vencem)
                2 -> Pretas sofreram xeque-mate. (Brancas vencem)
                3 -> Empate por afogamento. 
        """

        movimentos = []

        # É analisado todas as peças do tabuleiro individualmente
        for i in range(8):
            for j in range(8):
                posicao = str(i) + str(j)
                peca = self.tabuleiro.get_peca(posicao)

                # É visto se essa peça possui movimentos possíveis
                if peca and peca.cor == cor_jogador:
                    movimentos += self.calcular_movimento_jogo(posicao, cor_jogador)

        # Caso não haja nenhum movimento válido disponível, é considerado fim de jogo
        if movimentos == []:
            self.criar_copia_tabuleiro()
            self.verificar_xeque()

            # Se o jogador branco sofreu xeque, e não tem movimento para sair dele. Xeque-mate das pretas
            if cor_jogador == 0 and self.rei_branco_check == 1:
                return 1
            
            # Se o jogador preto sofreu xeque, e não tem movimento para sair dele. Xeque-mate das brancas
            elif cor_jogador == 1 and self.rei_preto_check == 1:
                return 2
            
            # Caso não haja xeque, e algum dos dois jogadores não tem mais movimentos disponiveís. Empate por afogamento
            else:
                return 3
            
        return 0

    def verificar_roque(self, cor_jogador):
        """
        Verifica se o roque (curto ou longo) é possível para o jogador.

        A verificação considera:
            - Se o rei está na posição inicial.
            - Se o rei e a torre correspondente nunca se moveram.
            - Se as casas entre rei e torre estão livres.

        Caso válido, adiciona a posição final do rei (curto ou longo) à sua lista de
        movimentos possíveis e atualiza a flag de roque.  
    
        Args:
            cor_jogador (int): Inteiro que representa a cor do jogador analisado (0 para branco, 1 para preto).
        """

        # Qual jogador deve ser verificado
        if cor_jogador == 0:

            # Se o jogador já rocou, retorna
            if self.roque_branco == 2:
                return
            
            # Pega a posição que o rei ocupa no começo do jogo, caso ele não esteja, é sinal que ele já seu moveu e não deve rocar
            rei_branco = self.tabuleiro.grid[7][4]

            # Verifica se ele está realmente nessa posição
            if rei_branco != None and type(rei_branco).__name__ == "King":

                # Verifica se ele já moveu. Ele pode andar pra frente e retornar pro mesmo lugar depois, nesse caso o roque não pode acontecer
                if rei_branco.mexeu == 0:

                    # Verifica se as posições do cavalo e do bispo estão vazias. Necessário para o roque
                    if self.tabuleiro.grid[7][5] == None and self.tabuleiro.grid[7][6] == None:

                        # Pega a torre, e faz a mesma verificação do rei
                        torre_branca_direita = self.tabuleiro.grid[7][7]
                        if torre_branca_direita != None and type(torre_branca_direita).__name__ == "Rook":
                            if torre_branca_direita.mexeu == 0:

                                # Caso tudo esteja correto, é armazenada a posição do roque e a flag é atualizada
                                rei_branco.lista_posicoes_validas.append("76")
                                self.roque_branco = 1

                    # É feita mesma verificação agora com a torre da esquerda           
                    if self.tabuleiro.grid[7][3] == None and self.tabuleiro.grid[7][2] == None and self.tabuleiro.grid[7][1] == None:
                        torre_branca_esquerda = self.tabuleiro.grid[7][0]

                        if torre_branca_esquerda != None and type(torre_branca_esquerda).__name__ == "Rook":

                            if torre_branca_esquerda.mexeu == 0:
                                rei_branco.lista_posicoes_validas.append("72")
                                self.roque_branco = 1

        
        # É feita a mesma verificação das brancas, agora com as pretas
        if cor_jogador == 1:
            if self.roque_preto == 2:
                return
            
            rei_preto = self.tabuleiro.grid[0][4]
            if rei_preto != None and type(rei_preto).__name__ == "King":
                if rei_preto.mexeu == 0:

                    if self.tabuleiro.grid[0][5] == None and self.tabuleiro.grid[0][6] == None:
                        torre_preta_direita = self.tabuleiro.grid[0][7]

                        if torre_preta_direita != None and type(torre_preta_direita).__name__ == "Rook":

                            if torre_preta_direita.mexeu == 0:
                                rei_preto.lista_posicoes_validas.append("06")
                                self.roque_preto = 1

                    if self.tabuleiro.grid[0][3] == None and self.tabuleiro.grid[0][2] == None and self.tabuleiro.grid[0][1] == None:
                        torre_preta_esquerda = self.tabuleiro.grid[0][0]

                        if torre_preta_esquerda != None and type(torre_preta_esquerda).__name__ == "Rook":

                            if torre_preta_esquerda.mexeu == 0:
                                rei_preto.lista_posicoes_validas.append("02")
                                self.roque_preto = 1

    def verificar_en_passant(self, posicao):
        """
        Verifica se é possível executar en passant para o peão na posição informada.

        A verificação considera:
            - A última jogada realizada (deve ser um peão adversário).
            - Se esse peão moveu exatamente duas casas.
            - Se existe um peão do jogador atual adjacente à coluna final do peão adversário.

        Caso, seja válido, adiciona à lista de movimentos do peão, o movimento
        de en passant e ativa a flag correspondente.

        Args:
            posicao (str): Posição no formato "xy".
        """

        # Atualiza a flag para zero
        self.en_passant = 0

        # Tenta-se pegar o último movimento, caso não seja possível, por ser a primeira jogada, retorna
        try:
            ultima_jogada = self.historico[self.turno - 1]
        except IndexError:
            return
        
        # Se a última peça movida, não foi um peão, o en passant é impossível, retorna
        if ultima_jogada[0] != "P":
            return
            
        # É analisada a cor do peão e a cor do jogador com base na cor do peão
        cor_peao = 0 if ultima_jogada[1] == "b" else 1
        cor_jogador = 1 - cor_peao    

        # Pega-se qual movimento o peão realizou por último
        origem = ultima_jogada[2:4]
        destino = ultima_jogada[4:6]

        # É se atribuído devidamente as linhas e a coluna
        linha_origem = int(origem[0])
        linha_destino = int(destino[0])
        coluna_destino = int(destino[1])

        # Caso o peão não andou duas casas (necessário para o en passant), retorna
        if abs(linha_origem - linha_destino) != 2:
            return
        
        # Se pega a direção do movimento do peão adversário
        direcao = -1 if cor_jogador == 0 else 1

        # Testa os peões adjacentes (esquerda e direita)
        for diferencial in [-1, 1]:
            coluna_lateral = coluna_destino + diferencial

            # Verifica se é uma coluna dentro do tabuleiro
            if 0 <= coluna_lateral <= 7:

                # Pega a posição dessa lateral
                posicao_lateral = str(linha_destino) + str(coluna_lateral)

                # Sendo uma possição diferente continua
                if posicao != posicao_lateral:
                    continue

                # É pego o peão lateral
                peao_lateral = self.tabuleiro.get_peca(posicao_lateral)

                # Verifica se realmente é um peão, e se ele pertence ao jogador adversário (aquele que irá fazer o en passant)
                if (peao_lateral != None and isinstance(peao_lateral, Pawn) and peao_lateral.cor == cor_jogador):

                    # Caso sim, é armazenada nas posições válidas do peão e a flag atualiza permitindo o en passant
                    posicao_en_passant = str(linha_destino + direcao) + str(coluna_destino)
                    peao_lateral.lista_posicoes_validas.append(posicao_en_passant)
                    self.en_passant = 1


    def verificar_promocao_peao(self):
        """
        Verifica se o peão chegou na posição necessária para poder ser promovido.

        A promoção ocorre quando:
            - Um peão branco alcança a linha 0.
            - Um peão preto alcança a linha 7.

        Caso seja possível, define a posição do peão em "self.promover_posicao".

        Returns:
            bool: Se True é possível realizar a promoção, caso False, não.
        """

        self.criar_copia_tabuleiro()

        # Percorre as duas pontas do mapa
        for i in range(8):

            # Pega-se a peça que ocupa essa posição
            peca = self.copia_grid[0][i]

            # Se for um peão e pertencer a cor contrária é atualizada a posição de promoção
            if type(peca).__name__ == "Pawn" and peca.cor == 0:
                self.promover_posicao = str(0) + str(i)
                return True
            
            # Faz-se a mesma verificação agora para o outro jogador
            peca = self.copia_grid[7][i]
            if type(peca).__name__ == "Pawn" and peca.cor == 1:
                self.promover_posicao = str(7) + str(i)
                return True
            
        return False
            

    def promover_peao(self, nova_peca):
        """
        Substitui o peão apto a ser promovido, por uma nova peça, escolhida pelo jogador.

        Atualiza:
            - Tabuleiro com a nova peça.
            - Histórico de jogadas.
            - Zera "self.promover_posicao".

        Args:
            nova_peca (str): Nome da peça para o qual o peão será promovido.
        """

        # Pega-se a posição do peão a ser promovido
        x, y = int(self.promover_posicao[0]), int(self.promover_posicao[1])

        # Pega-se a cor do peão em formato de int e string
        cor = self.tabuleiro.grid[x][y].cor
        cor_texto = "b" if cor == 0 else "p"

        # Caso a peça a substituir o peão é rainha
        if nova_peca == "queen":

            # É posicionada essa peça no tabuleiro original, no lugar do peão
            self.tabuleiro.posiciona_peca(Queen(cor, self.promover_posicao), self.promover_posicao)

            # É salvo o histórico com a promoção
            self.salvar_historico("P", cor_texto, self.promover_posicao, self.promover_posicao, promocao = True, peca_promovida = "Q")

        # É feito o mesmo procedimento agora com a torre
        elif nova_peca == "rook":
            self.tabuleiro.posiciona_peca(Rook(cor, self.promover_posicao), self.promover_posicao)
            self.salvar_historico("P", cor_texto, self.promover_posicao, self.promover_posicao, promocao = True, peca_promovida = "R")

        # Com o bispo
        elif nova_peca == "bishop":
            self.tabuleiro.posiciona_peca(Bishop(cor, self.promover_posicao), self.promover_posicao)
            self.salvar_historico("P", cor_texto, self.promover_posicao, self.promover_posicao, promocao = True, peca_promovida = "B")

        # E por último com o cavalo
        elif nova_peca == "horse":
            self.tabuleiro.posiciona_peca(Horse(cor, self.promover_posicao), self.promover_posicao)
            self.salvar_historico("P", cor_texto, self.promover_posicao, self.promover_posicao, promocao = True, peca_promovida = "H")

        # Depois de promovido, a posição a promover é zerada
        self.promover_posicao = None


    def salvar_historico(self, letra, cor, origem, destino, roque_branco = False, roque_preto = False, en_passant = False, promocao = False, peca_promovida = "", captura = False, letra_capturada = ""):
        """
        Salva a última jogada no histórico, utilizando notação simples.

        A string segue esse formato:
            "<letra><cor><origem><destino><especial>".

        Onde "<especial>" contém:
            - "x" -> indica xeque.
            - "r" -> roque curto, "R" -> roque longo.
            - "e" -> en passant.
            - "p<letra>" -> promoção para peça (Ex: "pQ" para rainha).
            - "c<letra>" -> captura de peça (Ex: "cR" para torre).

        Args:
            letra (str): A primeira letra do nome da peça.
            cor (str) A primeira letra da cor, "b" para branco, "p" para preto.
            origem (str): Posição em formato "xy", da posição atual da peça.
            destino (str): Posição em formato "xy", da posição futura da peça.
            roque_branco (bool): Flag que determina se a jogada foi um roque ou não.
            roque_preto (bool): Flag que determina se a jogada foi um roque ou não.
            en_passant (bool): Flag que determina se a jogada foi um en passant ou não.
            promocao (bool): Flag que determina se a peça foi promovida ou não.
            peca_promovida (str): A primeira letra da peça para o qual ela foi promovida.
            captura (bool): Flag que determina se a jogada foi uma captura ou não.
            letra_capturada (str): A primeira letra da peça que foi capturada.
        """

        # String que vai armazenar as jogadas especiais
        especial = ""

        # Se jogada resular em um xeque, é adicionado um "x"
        if self.rei_branco_check == 1 or self.rei_preto_check == 1:
            especial += "x"

        # Caso seja um roque, é adicionada um "R" para roque grande, e "r" para roque curto
        if roque_branco or roque_preto:
            especial += "R" if destino.endswith("2") else "r"

        # Se for um en passant, é adicionada um "e"
        if en_passant:
            especial += "e"

        # Agora se for uma promoção, é adicionado um "p"
        if promocao:
            especial += "p" + peca_promovida

            # Salva a composição da jogada com o "movimento"
            movimento = f"{letra}{cor}{origem}{destino}{especial}"

            # Caso seja um movimento duplicado, impede o armazenamento, pois configura um erro
            if self.historico and self.historico[-1] == movimento:
                return
            
            # Como a promoção acontece separadamente das outras jogadas, ela é armazenada no história e já é retornada
            self.historico.append(f"{letra}{cor}{origem}{destino}{especial}")

            # Contabiliza-se mais um para o turno
            self.turno += 1
            return
        
        # Caso seja uma captura, é adicionado o "c" juntamente da primeira letra da peça capturada
        if captura:
            especial += "c" + letra_capturada

        # É salva a composição da jogada com o "movimento"
        movimento = f"{letra}{cor}{origem}{destino}{especial}"

        # Impede salvar duplicamente
        if self.historico and self.historico[-1] == movimento:
            return
        
        # É guardada essa jogada no histórico
        self.historico.append(f"{letra}{cor}{origem}{destino}{especial}")

        # É contabalizada mais um para o turno
        self.turno += 1
    

    def salvar_partida(self, caminho_arquivo):
        """
        Salva o estado atual da partida em um arquivo JSON.

        O arquivo conterá:
            - Lista de peças em jogo (tipo, cor, posição e, para torres/reis, se já se moveram).
            - Turno atual.
            - Histórico completo de jogadas.

        Caso o diretório não exista, ele será criado automaticamente.

        Args:
            caminho_arquivo (str): Caminho completo do arquivo onde a partida será salva.
        """

        # Salva-se o número do turno, e o histórico da partida
        dados = {
            "pecas": [],
            "turno": self.turno,
            "historico": self.historico
            }
        
        # Vasculha-se o tabuleiro inteiro em busca das peças
        for i in range(8):
            for j in range(8):
                peca = self.tabuleiro.grid[i][j]

                # Se for o rei ou a torre, é salva o tipo, a cor, a posição e o atributo "mexeu"
                if type(peca).__name__ == "k" or type(peca).__name__ == "r":
                    dados["pecas"].append({
                        "tipo": type(peca).__name__.lower(),
                        "cor": peca.cor,
                        "posicao": str(i) + str(j),
                        "mexeu": peca.mexeu,
                    })

                # Caso seja as outras peças é salva os mesmos atributos com exceção de "mexeu" (elas não possuem)
                elif peca != None:
                    dados["pecas"].append({
                        "tipo": type(peca).__name__.lower(),
                        "cor": peca.cor,
                        "posicao": str(i) + str(j),
                    })
                
        # É pego o arquivo, e abre-se o caminho pra ele
        caminho_completo = caminho_arquivo
        os.makedirs(os.path.dirname(caminho_completo), exist_ok=True)

        # Escreve-se no arquivo todos os dados salvos
        with open(caminho_completo, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4)


    def carregar_partida(self, caminho_arquivo):
        """
        Carrega uma partida salva em arquivo JSON, restaurando o estado do jogo.

        A operação:
            - Limpa o tabuleiro atual.
            - Recria todas as peças com base nos dados salvos.
            - Restaura atributos especiais (ex.: `mexeu` para torres e reis).
            - Restaura histórico e turno.

        Args:
            caminho_arquivo (str): Caminho completo do arquivo salvo.

        Returns: 
            bool: True se o carregamento foi bem-sucedido.
        """

        # Abre o arquivo no formato de leitura
        with open(caminho_arquivo, "r", encoding = "utf-8") as f:
            dados = json.load(f)

        # Zera-se o tabuleiro original, para não interferir no processo de carregamento
        for i in range(8):
            for j in range(8):
                self.tabuleiro.grid[i][j] = None

        # Abre o dicionário, e pega-se todas as peças gravadas nele
        for peca_info in dados["pecas"]:

            # Pega os principais atributos
            tipo = peca_info["tipo"].lower()
            cor = peca_info["cor"]
            posicao = peca_info["posicao"]

            # Se for o rei ou a torre, pega o atributo "mexeu" também.
            if tipo == "king":

                # Grava a referência na váriavel peca
                peca = King(cor, posicao)
                peca.mexeu = peca_info.get("mexeu", 0)

            elif tipo == "rook":
                peca = Rook(cor, posicao)
                peca.mexeu = peca_info.get("mexeu", 0)

            elif tipo == "queen":
                peca = Queen(cor, posicao)

            elif tipo == "bishop":
                peca = Bishop(cor, posicao)

            elif tipo == "horse":
                peca = Horse(cor, posicao)

            elif tipo == "pawn":
                peca = Pawn(cor, posicao)

            else:
                continue

            # Depois de gravada na váriavel. Adiciona no tabuleiro devidamente a peça
            self.tabuleiro.posiciona_peca(peca, posicao)

        # Por último é pego o histórico e o turno
        self.historico = dados.get("historico", [])
        self.turno = dados.get("turno", 0)

        return True
    
    def voltar_jogada(self):
        """
        Desfaz a última jogada executada na partida.

        A ação considera todos os casos especiais:
            - Roque (curto e longo).
            - Captura.
            - Xeque.
            - En passant.
            - Promoção.

        A jogada é identificada pelo histórico e revertida no tabuleiro,
        restaurando peças capturadas ou movendo-as de volta.

        Se não houver jogadas para desfazer, apenas ignora.
        """

        # Flag para saber se a jogada foi um xeque
        jogada_xeque = False

        # Se o turno for menor que zero (impossível, afinal o jogo começa no turno zero), retorna
        if self.turno <= 0:
            return
        
        # Diminui um turno no total, para retornar ao estado do jogo antes dessa jogada
        self.turno -= 1

        # Tenta acessar esse elemento na lista, se não existir, é retornado
        try:
            ultima_jogada = self.historico[self.turno]
        except IndexError:
            return
        
        # É retirado esse elemento da lista
        self.historico.pop(self.turno)

        # Pega-se os principais atributos
        cor = 0 if ultima_jogada[1] == "b" else 1
        posicao_retornar = ultima_jogada[2:4]
        posicao_atual = ultima_jogada[4:6]

        # Tenta acessar uma possível jogada especial, se não aconteceu, apenas ignora
        try:
            especial = ultima_jogada[6]
        except IndexError:
            especial = ""

        # Pega-se a peça
        peca = self.tabuleiro.get_peca(posicao_atual)

        # Se a peça movida foi uma torre ou rei, diminui o atributo "mexeu"
        if type(peca).__name__[0].lower() == "r" or type(peca).__name__[0].lower() == "k":
            peca.mexeu -= 1

        # Se a jogada especial foi um xeque
        if especial == "x":

            # Tenta acessar a próxima jogada especial (o xeque antecede-se na denominação do histórico, e pode acontecer junto de outras jogadas especiais. Ex: "xR" xeque e roque longo)
            try:
                especial = ultima_jogada[7]
            except IndexError:
                # Caso não exista, ignora
                pass

            # Como o xeque aconteceu, a flag é acionada
            jogada_xeque = True

        # Se a jogada foi um roque longo
        if especial == "R":

            # é acessada qual a cor a executou (0 = brancas, 1 = pretas)
            if cor == 0:

                # O rei é movida de volta para o seu lugar
                self.tabuleiro.mover_peca(posicao_atual, posicao_retornar)

                # É pega a posição da torre
                peca = self.tabuleiro.get_peca("73")

                # Diminui o seu atributo "mexeu"
                peca.mexeu -= 1

                # A coloca de volta no seu lugar
                self.tabuleiro.mover_peca("73", "70")

                # Restaura o atributo "roque_branco"
                self.roque_branco = 0
                
                return
            
            # A mesma coisa acontece, agora com as pretas
            elif cor == 1:
                self.tabuleiro.mover_peca(posicao_atual, posicao_retornar)
                peca = self.tabuleiro.get_peca("03")
                peca.mexeu -= 1
                self.tabuleiro.mover_peca("03", "00")
                self.roque_preto = 0
                return

        # É feito o mesmo procedimento do roque longo, com o roque curto, a única exceção sendo que a posição deles é levemente diferente
        elif especial == "r":
            if cor == 0:
                self.tabuleiro.mover_peca(posicao_atual, posicao_retornar)
                peca = self.tabuleiro.get_peca("75")
                peca.mexeu -= 1
                self.tabuleiro.mover_peca("75", "77")
                self.roque_branco = 0
                return
            elif cor == 1:
                self.tabuleiro.mover_peca(posicao_atual, posicao_retornar)
                peca = self.tabuleiro.get_peca("05")
                peca.mexeu -= 1
                self.tabuleiro.mover_peca("05", "07")
                self.roque_preto = 0
                return

        # Caso a jogada seja uma captura
        elif especial == "c":

            # É pego a cor da peça capturada
            cor_oposta = 1 - peca.cor

            # A peça que a capturou volta para seu lugar anterior
            self.tabuleiro.mover_peca(posicao_atual, posicao_retornar)

            # Pega-se a peça capturada, caso a captura tenha acontecido junto de um xeque, é preciso pegar uma casa pra frente.
            peca_comida = ultima_jogada[7]
            if jogada_xeque == True:
                peca_comida = ultima_jogada[8]

            # Se a peça comida foi um peão
            if peca_comida == "P":

                # Coloca-se ela no seu lugar anterior
                self.tabuleiro.posiciona_peca(Pawn(cor_oposta, posicao_atual), posicao_atual)

                # Remove ela da lista de materiais perdidos
                self.verificar_material_fora_de_campo(cor_oposta, peca_comida, remover = True)

            # Se a peça for uma torre
            elif peca_comida == "R":
                self.tabuleiro.posiciona_peca(Rook(cor_oposta, posicao_atual), posicao_atual)
                self.verificar_material_fora_de_campo(cor_oposta, peca_comida, remover = True)

            # Se a peça for um cavalo
            elif peca_comida == "H":
                self.tabuleiro.posiciona_peca(Horse(cor_oposta, posicao_atual), posicao_atual)
                self.verificar_material_fora_de_campo(cor_oposta, peca_comida, remover = True)

            # Se a peça for um bispo
            elif peca_comida == "B":
                self.tabuleiro.posiciona_peca(Bishop(cor_oposta, posicao_atual), posicao_atual)
                self.verificar_material_fora_de_campo(cor_oposta, peca_comida, remover = True)

            # Se a peça for uma rainha
            elif peca_comida == "Q":
                self.tabuleiro.posiciona_peca(Queen(cor_oposta, posicao_atual), posicao_atual)
                self.verificar_material_fora_de_campo(cor_oposta, peca_comida, remover = True)

            return
              
        # Caso a jogada seja um en passant
        elif especial == "e":

            # Pega-se a cor oposta
            cor_oposta = 1 - peca.cor

            # Move-se o peão que capturou de volta ao seu lugar anterior
            self.tabuleiro.mover_peca(posicao_atual, posicao_retornar)

            # É pega a linha, a coluna e a direção
            linha_atual = int(posicao_atual[0])
            coluna_atual = posicao_atual[1]
            direcao = -1 if peca.cor == 0 else 1

            # É calculada a posição que o peão capturado se encontrava antes
            posicao_peao_comido = str(linha_atual - direcao) + coluna_atual

            # O peão que foi capturado é posicionada no seu lugar anterior
            self.tabuleiro.posiciona_peca(Pawn(cor_oposta, posicao_peao_comido), posicao_peao_comido)

            # Ele é retirado da lista de peças perdidas
            self.verificar_material_fora_de_campo(cor_oposta, peca_comida = "P", remover = True)
            return
        
        # Caso seja uma promoção
        elif especial == "p":

            # É pego a posição que o peão se promoveu, para poder ser promovido novamente
            self.promover_posicao = posicao_retornar

            # A peça promivida, volta a ser um peão
            self.tabuleiro.posiciona_peca(Pawn(cor, self.promover_posicao), self.promover_posicao)
            return

        # Caso não haja nenhum movimento especial, a peça simplesmente retorna para o seu lugar anterior
        self.tabuleiro.mover_peca(posicao_atual, posicao_retornar)

    def jogar_ia(self):
        """
        Método responsável por calcular e executar a jogada da IA.

        Processo:
            - A ia simula uma série de jogadas com base no estado atual do tabuleiro.
            - Ela através de seus métodos de avaliação, escolhe a jogada que trará mais resultado.
            - Executa essa jogada escolhida no tabuleiro real.

        Returns:
            str: Movimento escolhido no formato "origemdestino" (Ex: "0406").
        """

        # A ia simula uma série de jogadas
        self.ia.simular_jogada()

        # Ela aplica essa jogada, e gera a sua recompensa
        self.ia.aplicar_jogada_escolhida()

        # O movimento é avaliado, e é retornado em forma de string
        movimento = self.ia.avaliar_movimento()

        # Se o movimento existir
        if movimento:

            # É separada a origem do movimento, e o seu destino
            origem = movimento[:2]
            destino = movimento[2:]

            # A jogada é executada
            self.mover_peca_jogo(origem, destino)

            # É retornada a string concatenada da jogada
            return f"{origem}{destino}"

    def colocar_peca_promovida_ia(self, cor, posicao):
        """
        Promove automaticamente um peão da IA para rainha (escolha fixa)

        Args:
            cor (int): Cor da peça (0 = branco, 1 = preto).
            posicao (str): Posição do peão a ser promovido.
        """

        self.tabuleiro.posiciona_peca(Queen(cor, posicao), posicao)

    def reiniciar(self):
        """
        Reinicia a partida para o estado inicial

        A operação:
            - Reseta o tabuleiro para a sua posição inicial.
            - Limpa as listas das peças perdidas.
            - Zera as flags e variáveis de controle (roque, en passant, promoção, histórico, turno).
        """

        # O Tabuleiro retorna para a sua posição inicial
        self.tabuleiro.reiniciar()
        self.inicializar_pecas()

        # Zera todos os atributos
        self.copia_grid = [[None for _ in range (8)] for _ in range(8)]
        self.posicao_rei_branco = 0
        self.posicao_rei_preto = 0
        self.posicao_teste_rei_preto = 0
        self.posicao_teste_rei_branco = 0
        self.rei_branco_check = 0
        self.rei_preto_check = 0
        self.roque_branco = 0
        self.roque_preto = 0
        self.en_passant = 0
        self.promover_posicao = 0
        self.lista_pecas_perdidas_brancas.clear()
        self.lista_pecas_perdidas_pretas.clear()
        self.historico = []
        self.turno = 0

    def verificar_insuficiencia_de_material(self):
        """
        Verifica possíveis empates por insufiência de material com base nas regras do Xadrez.

        Situações consideras empates:
            - Apenas os dois reis.
            - Rei + 1 bispo vs rei.
            - Rei + 1 cavalo vs rei.
            - Rei + 1 bispo vs rei + 1 bispo, se os bispos estiverem em casas da mesma cor.
            - Rei + 1 cavalo vs rei + 1 cavalo.

        O processo acontece:
            - É contado quantas peças de cada tipo ainda existe no tabuleiro.
            - Caso não exista o número suficiente do tipo de peças, o jogo é terminado em empate.

        Returns:
            str: "EMPATE" se não há material suficiente para xeque-mate,
                "SEM EMPATE" caso contrário.
        """

        # Inicializa os contadores das peças
        cont_bispo = []
        cont_peao = 0
        cont_cavalo = 0
        cont_torre = 0
        cont_rainha = 0

        # Verifica-se todo o tabuleiro
        for i in range(8):
            for j in range(8):
                peca = self.tabuleiro.grid[i][j]
                if peca != None:

                    # Extrai-se o nome da peça
                    nome = type(peca).__name__.upper()

                    # Conta-se quantas peças há de cada tipo
                    if nome == "BISHOP":
                        cont_bispo.append((i, j))
                    elif nome == "PAWN":
                        cont_peao += 1
                    elif nome == "HORSE":
                        cont_cavalo += 1
                    elif nome == "ROOK":
                        cont_torre += 1
                    elif nome == "QUEEN":
                        cont_rainha += 1

        # É calculado o total de peças
        total_pecas = len(cont_bispo) + cont_cavalo + cont_torre + cont_rainha + cont_peao

        # Caso só exista os reis em jogo, é empate
        if total_pecas == 0:
            return "EMPATE"
        
        # Se existir qualquer peão, torre ou rainha, ainda há chance de xeque-mate
        if cont_peao > 0 or cont_torre > 0 or cont_rainha > 0:
            return "SEM EMPATE"
        
        # Caso só exista um bispo ou só um cavalo em jogo, é empate
        if total_pecas == 1 and (len(cont_bispo) == 1 or cont_cavalo == 1):
            return "EMPATE"
        
        # Verifica se os bispos são da mesma cor de casa, se sim, é empate
        if len(cont_bispo) == 2 and total_pecas == 2:
            cores = []
            for linha, coluna in cont_bispo:

                # Extraimos qual cor de casa ele está
                cor_casa = (linha + coluna) % 2

                # Adicionamos em uma lista
                cores.append(cor_casa)
            
            # Verifica se estão na mesma casa
            if cores[0] == cores[1]:
                return "EMPATE"
            
        # Se nenhuma das condições é sanada, o jogo continua
        return "SEM_EMPATE"
    
    def verificar_material_fora_de_campo(self, cor_oposta = 0, peca_comida = "", remover = False):
        """
        Atualiza a lista de peças perdidas de cada jogador.

        Se "remover" for False:
            - Verifica a última jogada no histórico.
            - Se houve captura, adiciona a peça capturada à lista correspondente.

        Se "remover" for True:
            - Remove uma peça específica da lista (usado para desfazer jogadas).

        Args:
            cor_oposta (int): Cor da peça perdida.
            peca_comida (str): Letra identificado da peça (Ex: "P" para peão).
            remover (bool): True para remover peça da lista, False para adicionar.
        """

        # Verifica se é pra adicionar uma peça
        if remover == False:

            # Tenta acessar a última jogada, se existir
            try:
                ultimo_movimento = self.historico[self.turno - 1]
            except IndexError:
                return
            
            # Verifica se houve captura no último movimento
            if "c" in ultimo_movimento:

                # É pego a cor da peça capturada, e a primeira letra do seu nome
                cor = ultimo_movimento[1]
                peca_capturada = ultimo_movimento[-1]
                cor_capturada = 0 if cor == "p" else 1

                # Se for uma peça das brancas, é adicionada a lista de peças perdidas das brancas
                if cor_capturada == 0:
                    self.lista_pecas_perdidas_brancas.append(f"{peca_capturada}{cor_capturada}")

                # Se for uma peça das pretas, é adicionada a lista de peças perdidas das pretas
                else:
                    self.lista_pecas_perdidas_pretas.append(f"{peca_capturada}{cor_capturada}")

        # Caso seja para remover uma peça que foi comida (através do voltar jogada)
        else:

            # O processo é o mesmo, porém agora é feita apenas a remoção ao invés da adição
            if cor_oposta == 0:
                self.lista_pecas_perdidas_brancas.remove(f"{peca_comida}{cor_oposta}")
            elif cor_oposta == 1:
                self.lista_pecas_perdidas_pretas.remove(f"{peca_comida}{cor_oposta}")