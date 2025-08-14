# Imports necessários
from pieces import *
import copy

class IA:
    """
    Classe IA.

    Controladora principal responsável por controlar a inteligência artificial do jogo de xadrez.

    Executa simulações de jogadas em diferentes níveis de profundidade, garantindo que
    apenas movimentos válidos sejam executado. Interage com o sistema Q-Learning para tomada
    de decisões baseadas em aprendizagem por reforço.
    """

    def __init__(self, jogo, cor_ia = 1):
        """
        Inicialza a IA juntamente de seus atributos.

        Args:
            jogo (Game): Instância da classe Game, contendo o estado do jogo.
            cor_ia (int, optional): Representa a cor que a IA irá jogar nessa partida. (0 para branco, 1 para preto). Default é 1.
        """

        # Atribuição do Game, da cor e a criação da lista de jogadas
        self.jogo = jogo
        self.cor = cor_ia
        self.lista_jogadas_possiveis = []

        # Criação e atribuição do QLearning (Classe responsável pelas decições e o aprendizado)
        self.qlearning = QLearning(self.jogo)

    def simular_jogada(self):   
        """
        Realiza simulação de jogadas em três níveis de profundidade,
        ou seja, IA -> JOGADOR -> IA.

        Para cada sequência completa, armazena o estado final do tabuleiro junto
        dos movimentos inicias executados pelas simulações.

        As jogadas são podadas com base em uma heurística de valor, para evitar simulações gigantescas irrelevantes.
        """

        # Limpa o "lista_jogadas_possiveis" para começar zerado
        self.lista_jogadas_possiveis.clear()    

        # Inicializa os principais atributos, o tabuleiro e as flags necessárias para as simulações
        self.inicializar_tabuleiro_e_flags()

        # Nível 1 Jogada da IA - Vasculha todas as casas do tabuleiro copiado
        for i in range(8):
            for j in range(8):
                peca = self.copia_grid[i][j]

                # Verifica se é uma peça, e se pertence ao computador
                if peca != None and peca.cor == self.cor:

                    # Pega-se a posição
                    posicao = str(i) + str(j)

                    # É calculado e armazenado os movimentos dessa peça dentro de "moveset"
                    moveset = list(self.calcular_movimento(posicao, self.cor))

                    # Caso ela não tenha movimentos possíveis, pula
                    if not moveset:
                        continue

                    # Poda: Simula apenas os 5 melhores movimentos
                    moveset.sort(key = lambda m: self.valor_movimento(posicao, m), reverse = True)
                    moveset = moveset[:5]

                    # É feita uma cópia para salvar os atributos antes de modifica-los
                    copia_profundidade_1 = self.copiar_tabuleiro_e_flags()

                    # Agora analisa-se todos os movimentos calculados dessa peça
                    for m in moveset:
                        destino = m
                        origem = str(i) + str(j)

                        # O movimento analisado é executado
                        self.mover_peca_ia(origem, destino)

                        # É verificado se é possível promover o peão
                        if self.verificar_promocao_peao() == True:
                            self.promover_peao()

                        # Nível 2 Jogada do Jogador - Vasculha todas as casas do tabuleiro copiado
                        for k in range(8):
                            for l in range(8):
                                peca_2 = self.copia_grid[k][l]

                                # É feito o mesmo procedimento de antes, agora procurando apenas por peças do jogador
                                cor = 1 - self.cor
                                if peca_2 != None and peca_2.cor == cor:
                                    posicao_2 = str(k) + str(l)
                                    moveset_2 = list(self.calcular_movimento(posicao_2, cor))
                                    if not moveset_2:
                                        continue

                                    moveset_2.sort(key = lambda m: self.valor_movimento(posicao_2, m), reverse = True)
                                    moveset_2 = moveset_2[:1]
                                    
                                    copia_profundidade_2 = self.copiar_tabuleiro_e_flags()
                                    for n in moveset_2:
                                        destino_2 = n
                                        origem_2 = str(k) + str(l)
                                        self.mover_peca_ia(origem_2, destino_2)

                                        if self.verificar_promocao_peao() == True:
                                            self.promover_peao()

                                        # Nível 3 Jogada da IA - Vasculha novamente todas as casas do tabuleiro copiado
                                        for z in range(8):
                                            for x in range(8):
                                                peca_3 = self.copia_grid[z][x]
                                                if peca_3 != None and peca_3.cor == self.cor:
                                                    posicao_3 = str(z) + str(x)
                                                    moveset_3 = list(self.calcular_movimento(posicao_3, self.cor))
                                                    if not moveset_3:
                                                        continue

                                                    moveset_3.sort(key = lambda m: self.valor_movimento(posicao_3, m), reverse = True)
                                                    moveset_3 = moveset_3[:1]

                                                    copia_profundidade_3 = self.copiar_tabuleiro_e_flags()
                                                    for y in moveset_3:
                                                        destino_3 = y
                                                        origem_3 = str(z) + str(x)
                                                        self.mover_peca_ia(origem_3, destino_3)

                                                        if self.verificar_promocao_peao() == True:
                                                            self.promover_peao()

                                                        # Após os 3 níveis de execução serem concluídos uma vez, é armazenado em uma dicionário, o movimento inicial, e o estado do tabuleiro que foi chegado
                                                        movimento = origem + destino
                                                        tabuleiro = self.salvar_tabuleiro()
                                                        self.lista_jogadas_possiveis.append({"tipo": "movimento",
                                                                                            "movimento": movimento,
                                                                                            "tabuleiro": tabuleiro})
                                                        
                                                        # As flags e o tabuleiro são restaurados para o seu anterior dentro do nível 3
                                                        self.restaurar_tabuleiro_e_flags(copia_profundidade_3)

                                        # As flags e o tabuleiro são restaurados para o seu anterior dentro do nível 2
                                        self.restaurar_tabuleiro_e_flags(copia_profundidade_2)

                        # As flags e o tabuleiro são restaurados para o seu anterior dentro do nível 1
                        self.restaurar_tabuleiro_e_flags(copia_profundidade_1)

    def valor_movimento(self, origem, destino):
        """
        Avalia a relevância de um movimento baseada em heurística simples.

        Critérios avaliados:
            - Captura de peça (peso baseado no valor da peça capturada).
            - Centralização (domínio do centro do tabuleiro).
            - Promoção de peão.
            - Desenvolvimento inicial das peças.

        Args:
            origem (str): Posição de origem no formato "xy".
            destino (str): Posição de destino no formato "xy".

        Returns:
            int: Valor heurístico atríbuido a possível jogada.
        """

        valor = 0

        # Captura de peças
        peca_destino = self.get_peca(destino)
        if peca_destino != None:
            nome = type(peca_destino).__name__.upper()
            valores_pecas = {
                "PAWN": 1,
                "HORSE": 3,
                "BISHOP": 3,
                "TOWER": 5,
                "QUEEN": 9,
                "KING": 60
            }

            # É pego o valor da peça e multiplicado por um peso comum
            valor += valores_pecas.get(nome, 0) * 10 

        # Centralização da peça
        linha, coluna = int(destino[0]), int(destino[1])
        if 2 <= linha <= 5 and 2 <= coluna <= 5:
            valor += 5

        # Promoção de peão
        peca_origem = self.get_peca(origem)
        if type(peca_origem).__name__.upper() == "PAWN":
            if (peca_origem.cor == 0 and linha == 0) or (peca_origem.cor == 1 and linha == 7):
                valor += 20
        
        # Desenvolvimento do bispo e do cavalo
        if type(peca_origem).__name__.upper() in ("HORSE", "BISHOP") and (
        (peca_origem.cor == 0 and int(origem[0]) == 7) or
        (peca_origem.cor == 1 and int(origem[0]) == 0)):
            valor += 6

        # Salva estado atual do xeque
        estado_xeque_branco = self.rei_branco_check
        estado_xeque_preto = self.rei_preto_check

        # Verifica se o movimento é xeque
        self.criar_copia_tabuleiro_copiado()
        self.posiciona_peca_copiado(peca_origem, destino)
        self.posiciona_peca_copiado(None, origem)
        self.verificar_xeque()
        if peca_origem.cor == 0 and self.rei_preto_check == 1:
                valor += 50
        elif peca_origem.cor == 1 and self.rei_branco_check == 1:
                valor += 50

        # Restaura estado original
        self.rei_branco_check = estado_xeque_branco
        self.rei_preto_check = estado_xeque_preto

        return valor

    def inicializar_tabuleiro_e_flags(self):
        """
        Inicializa a cópia do tabuleiro e de todos os atributos relevantes para o jogo.

        Usado para isolar simulações e preservar o estado real do jogo intacto.

        Attributes:
            copia_grid (list[list]): Cópia do tabuleiro para simulações de jogadas.
            posicao_rei_branco (str): Posição atual do rei branco.
            posicao_rei_preto (str): Posição atual do rei preto.
            posicao_teste_rei_branco (str): Posição de teste do rei branco.
            posicao_teste_rei_preto (str): Posição de teste do rei preto.
            rei_branco_check (int): Indica se o rei branco está em xeque (1 = sim, 0 = não).
            rei_preto_check (int): Indica se o rei preto está em xeque (1 = sim, 0 = não).
            roque_branco (int): Flag que indica possibilidade de roque das brancas.
            roque_preto (int): Flag que indica possibilidade de roque das pretas.
            en_passant (int): Flag que indica possibilidade de en passant.
            promover_posicao (str): Posição de um peão apto à promoção.
            turno (int): Contador do turno atual.
            historico (list): Lista de jogadas executadas.
        """

        self.copia_grid = copy.deepcopy(self.jogo.tabuleiro.grid)
        self.posicao_rei_branco = copy.deepcopy(self.jogo.posicao_rei_branco)
        self.posicao_rei_preto = copy.deepcopy(self.jogo.posicao_rei_preto)
        self.posicao_teste_rei_branco = copy.deepcopy(self.jogo.posicao_teste_rei_branco)
        self.posicao_teste_rei_preto = copy.deepcopy(self.jogo.posicao_teste_rei_preto)
        self.rei_branco_check = copy.deepcopy(self.jogo.rei_branco_check)
        self.rei_preto_check = copy.deepcopy(self.jogo.rei_preto_check)
        self.roque_branco = copy.deepcopy(self.jogo.roque_branco)
        self.roque_preto = copy.deepcopy(self.jogo.roque_preto)
        self.en_passant = copy.deepcopy(self.jogo.en_passant)
        self.promover_posicao = copy.deepcopy(self.jogo.promover_posicao)
        self.turno = copy.deepcopy(self.jogo.turno)
        self.historico = copy.deepcopy(self.jogo.historico)

    def copiar_tabuleiro_e_flags(self):
        """
        Cópia os atributos e o tabuleiro, direto para um dicionário através do deepcopy,
        com o objetivo de persistir os dados ao longos das simulações.

        Returns:
            dict: Dicionário, com todos os atributos salvos para a restauração futura.
        """

        return {
            "tipo": "copia",
            "tabuleiro": copy.deepcopy(self.copia_grid),
            "posicao_rei_branco": copy.deepcopy(self.posicao_rei_branco),
            "posicao_rei_preto": copy.deepcopy(self.posicao_rei_preto),
            "posicao_teste_rei_branco": copy.deepcopy(self.posicao_teste_rei_branco),
            "posicao_teste_rei_preto": copy.deepcopy(self.posicao_teste_rei_preto),
            "rei_branco_check": copy.deepcopy(self.rei_branco_check),
            "rei_preto_check": copy.deepcopy(self.rei_preto_check),
            "roque_branco": copy.deepcopy(self.roque_branco),
            "roque_preto": copy.deepcopy(self.roque_preto),
            "en_passant": copy.deepcopy(self.en_passant),
            "promover_posicao": copy.deepcopy(self.promover_posicao),
            "turno": copy.deepcopy(self.turno),
            "historico": copy.deepcopy(self.historico),
        }
    
    def restaurar_tabuleiro_e_flags(self, dicionario):
        """
        Restaura o estado do tabuleiro e as flags a partir de uma cópia previamente salva.

        Args:
            dicionario (dict): Dicionário onde todos os atributos estavam salvos, 
            obtida através de "copiar_tabuleiro_e_flags.
        """

        if dicionario["tipo"] != "copia":
            return
        self.copia_grid = copy.deepcopy(dicionario["tabuleiro"])
        self.posicao_rei_branco = copy.deepcopy(dicionario["posicao_rei_branco"])
        self.posicao_rei_preto = copy.deepcopy(dicionario["posicao_rei_preto"])
        self.posicao_teste_rei_branco = copy.deepcopy(dicionario["posicao_teste_rei_branco"])
        self.posicao_teste_rei_preto = copy.deepcopy(dicionario["posicao_teste_rei_preto"])
        self.rei_branco_check = copy.deepcopy(dicionario["rei_branco_check"])
        self.rei_preto_check = copy.deepcopy(dicionario["rei_preto_check"])
        self.roque_branco = copy.deepcopy(dicionario["roque_branco"])
        self.roque_preto = copy.deepcopy(dicionario["roque_preto"])
        self.en_passant = copy.deepcopy(dicionario["en_passant"])
        self.promover_posicao = copy.deepcopy(dicionario["promover_posicao"])
        self.turno = copy.deepcopy(dicionario["turno"])
        self.historico = copy.deepcopy(dicionario["historico"])

    def criar_copia_tabuleiro_copiado(self):
        """
        Cria uma cópia da cópia do tabuleiro através do deepcopy.

        Necessário para fazer validações temporárias (Ex: Xeque).
        """

        self.copia_copia_grid = copy.deepcopy(self.copia_grid)

    def aplicar_jogada_escolhida(self):
        """
        Executa a jogada escolhida pela IA e atualiza o sistema de aprendizagem por reforço.

        A jogada é executada no tabuleiro copiado, e o estados (antes e depois) são usados
        no Q-Learning para atualizar a Q-table com base na recompensa obtida.
        """

        # Avalia-se o movimento e escolhe, armazenando-o em "movimento"
        movimento = self.avaliar_movimento()

        # Caso não exista um, impede de gerar erro, retorna
        if not movimento:
            return
        
        # É salvo o estado antigo e o tabuleiro, antes de realizar o movimento
        estado_antigo = self.qlearning.gerar_estado(self, self.copia_grid, self.cor)
        tabuleiro_antigo = self.salvar_tabuleiro()

        # Extrai a origem e o destino, e realiza o movimento
        origem = movimento[:2]
        destino = movimento[2:]
        self.mover_peca_ia(origem, destino)

        # É salvo o novo tabuleiro e o estado, após o movimento ser realizada
        tabuleiro_novo = self.salvar_tabuleiro()
        novo_estado = self.qlearning.gerar_estado(self, self.copia_grid, self.cor)

        # Todas as outras possíveis ações são salvas
        acoes_novas = [mov["movimento"] for mov in self.lista_jogadas_possiveis]

        # A recompensa é calculada
        recompensa = self.qlearning.calcular_recompensa(self, tabuleiro_antigo, tabuleiro_novo)

        # O QLearning é atualizado com a nova jogada e depois é salvo
        self.qlearning.atualizar(estado_antigo, movimento, recompensa, novo_estado, acoes_novas)
        self.qlearning.salvar_q_table()

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
                if self.copia_grid[x][y] != None:
                    peca = self.copia_grid[x][y]
                    letra = type(peca).__name__[0]
                    cor = 'b' if peca.cor == 0 else 'p'
                    linha += " " + letra + cor + " "
                else:
                    linha += " -- "
            print(linha)
            cont += 1

    def salvar_tabuleiro(self):
        """
        Salva o estado atual do tabuleiro copiado como uma lista de dicionários.

        Cada peça é representada como "<letra><cor><x><y>":
            - letra (str): Primeira letra do nome da peça.
            - Cor (int): Inteiro que representa a cor da peça.
            - X (int): Posição da linha em que a peça está.
            - Y (int): Posição da coluna em que a peça está.

        Returns:
            list[dict]: Lista de dicionários contendo todas as peças presentes no estado do tabuleiro.
        """

        # Cria a lista para armazenar as peças
        lista = []

        # Percorre todo o tabuleiro copiado em busca das peças
        for x in range(8):
            for y in range(8):
                peca = self.copia_grid[x][y]

                # Pega apenas as peças
                if peca != None:
                    
                    # Pega-se a primeira letra do nome e a sua cor
                    letra = type(peca).__name__[0].upper()
                    cor = peca.cor

                    # A peça é armazenada na lista
                    lista.append({"letra": letra, "cor": cor, "x": x, "y": y})

        return lista
    
    def avaliar_movimento(self):
        """
        Avalia os movimentos que foram simulados, e escolhe um 
        baseada na política de Q-Learning.

        Returns:
            str | None: Movimento escolhido no formato "origemdestino" (Ex: "2030"),
            ou None se não houver movimentos disponíveis.
        """

        # Salva o estado atual do tabuleiro
        estado = self.qlearning.gerar_estado(self, self.copia_grid, self.cor)

        # Pega-se todos os movimentos presentes na "lista_jogadas_possiveis"
        acoes_possiveis = [mov["movimento"] for mov in self.lista_jogadas_possiveis]

        # Caso não exista nenhum, retorna para impedir erro
        if not acoes_possiveis:
            return None
        
        # Retorna o movimento escolhido
        return self.qlearning.escolher_acao(estado, acoes_possiveis)
    
    def get_peca(self, posicao):
        """
        Retorna a peça que está armazenada em uma determinada posição na cópia do tabuleiro.

        Args:
            posicao (str): Posição no formato "xy".

        Returns:
            Object | None: Instância da peça, ou None se a casa estiver vazia.
        """

        x, y = int(posicao[0]), int(posicao[1])
        return self.copia_grid[x][y]
    
    def posiciona_peca(self, peca, posicao):
        """
        Posiciona uma determinada peça em uma posição específica na cópia do tabuleiro (Ex: "04").

        Args:
            peca (object | None): Instância da peça a ser posicionada, ou None se for remover.
            posicao (str): Posição concatenada de dois números, onde o primeiro representa o x e o segundo o y.
        """
        x, y = int(posicao[0]), int(posicao[1])
        self.copia_grid[x][y] = peca

    def posiciona_peca_copiado(self, peca, posicao):
        """
        Posiciona uma determinada peça em uma posição específica na cópia da cópia do tabuleiro (Ex: "04")
        Usado em vericações de Xeque.

        Args:
            peca (object | None): Instância da peça a ser posicionada, ou None se for remover.
            posicao (str): Posição concatenada de dois números, onde o primeiro representa o x e o segundo o y.
        """
        x, y = int(posicao[0]), int(posicao[1])
        self.copia_copia_grid[x][y] = peca

    def calcular_movimento(self, posicao, cor):
        """
        Calcula todos os movimentos válidos para a peça em uma posição.

        O cálculo considera movimentos padrões, e jogadas especiais. 
        Além de bloquear movimentos ilegais.

        Args:
            posicao (str): Posição no formato "xy".
            cor_jogador (int): Cor do jogador a ter seu movimento calculado,
            representada por um inteiro. (0 para branco, 1 para preto).

        Returns:
            list[str]: Lista de posições válidas para a peça, lista vazia caso a peça não possua movimentos.
        """

        # É armazenado para testar as posições atuais dos reis
        self.posicao_teste_rei_preto = self.posicao_rei_preto
        self.posicao_teste_rei_branco = self.posicao_rei_branco

        movimentos = []

        # Pega a peça
        peca = self.get_peca(posicao)
        if peca == None:
            return "99"

        # Calcula a lista de seus movimentos
        peca.movimento(self.copia_grid)

        # Caso seja um rei, é verificado a possibilidade de fazer um roque
        if type(peca).__name__[0].lower() == "k":
            self.verificar_roque(cor)

        self.verificar_en_passant(posicao)

        moveset = list(peca.lista_posicoes_validas)

        # É analisada individualmente cada possível movimento
        for m in moveset:
            self.criar_copia_tabuleiro_copiado()
            origem = posicao
            destino = m

            # Caso seja um rei é necessário atualizar a posição de teste
            if type(peca).__name__.lower() == "king":
                if peca.cor == 0:
                    self.posicao_teste_rei_branco = destino
                else:
                    self.posicao_teste_rei_preto = destino

            # É colocada a peça nessa nova posição no tabuleiro simulado
            self.posiciona_peca_copiado(peca, destino)
            self.posiciona_peca_copiado(None, origem)

            # Verifica-se o xeque
            self.verificar_xeque()

            # Caso não seja um movimento ilegal é armazenada como válido
            if self.rei_branco_check == 0 and cor == 0:
                movimentos.append(m)
            if self.rei_preto_check == 0 and cor == 1:
                movimentos.append(m)

        return movimentos
    
    def verificar_xeque(self):
        """
        Verifica se algum dos reis sofreu um xeque após o último movimento executado.

        Percorre todas as peças no tabuleiro copiado, calcula seus movimentos e identifica se alguma
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
                peca = self.copia_copia_grid[i][j]
                if peca != None:
                    
                    # Se algum dos possíveis movimento dessa peça ameaçar o rei, é considerado xeque
                    peca.movimento(self.copia_copia_grid)
                    moveset = list(peca.lista_posicoes_validas)

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

    def mover_peca_ia(self, origem, destino):
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
        peca_destino_antes = self.get_peca(destino)
        houve_captura = peca_destino_antes is not None
        peca_capturada_letra = type(peca_destino_antes).__name__[0].upper() if houve_captura else ""

        # É pego os outros atributos necessários
        peca = self.get_peca(origem)
        letra = type(peca).__name__[0].upper()
        cor = "b" if peca.cor == 0 else "p"

        # Caso seja uma torre ou o rei, é necessário contabilizar o atributo "mexeu"
        if type(peca).__name__.lower() in ["king", "rook"]:
            peca.mexeu += 1

            # Se for um roque curto das pretas
            if origem == "74" and destino == "76" and self.roque_branco:

                # Move a peça no tabuleiro original
                self.mover_peca(origem, destino, roque_branco = True)

                # Atualiza o atributo
                self.roque_branco == 2

                # Cria uma cópia e verifica se foi uma jogada que resulta em xeque
                self.criar_copia_tabuleiro_copiado()
                self.verificar_xeque()

                # Salva o histórico com os atributos necessários
                self.salvar_historico(letra, cor, origem, destino, roque_branco = True, captura = houve_captura, letra_capturada = peca_capturada_letra)
                return True
            
            # Se for um roque longo das pretas
            if origem == "74" and destino == "72" and self.roque_branco:
                self.mover_peca(origem, destino, roque_branco = True)
                self.roque_branco == 2
                self.criar_copia_tabuleiro_copiado()
                self.verificar_xeque()
                self.salvar_historico(letra, cor, origem, destino, roque_branco = True, captura = houve_captura, letra_capturada = peca_capturada_letra)
                return True
            
            # Se for um roque curto das brancas
            if origem == "04" and destino == "06" and self.roque_preto:
                self.mover_peca(origem, destino, roque_preto = True)
                self.roque_preto == 2
                self.criar_copia_tabuleiro_copiado()
                self.verificar_xeque()
                self.salvar_historico(letra, cor, origem, destino, roque_preto = True, captura = houve_captura, letra_capturada = peca_capturada_letra)
                return True
            
            # Se for um roque longo das brancas
            if origem == "04" and destino == "02" and self.roque_preto:
                self.mover_peca(origem, destino, roque_preto = True)
                self.roque_preto == 2
                self.criar_copia_tabuleiro_copiado()
                self.verificar_xeque()
                self.salvar_historico(letra, cor, origem, destino, roque_preto = True, captura = houve_captura, letra_capturada = peca_capturada_letra)
                return True

        # Se for um en passant
        if self.en_passant:
            self.mover_peca(origem, destino, en_passant = True)
            self.criar_copia_tabuleiro_copiado()
            self.verificar_xeque()
            self.salvar_historico(letra, cor, origem, destino, en_passant = True, captura = houve_captura, letra_capturada = peca_capturada_letra)
            return True

        # Caso seja uma jogada comum (captura / movimento)
        self.mover_peca(origem, destino)
        self.criar_copia_tabuleiro_copiado()
        self.verificar_xeque()
        self.salvar_historico(letra, cor, origem, destino, captura = houve_captura, letra_capturada = peca_capturada_letra)
        return True
    
    def mover_peca(self, origem, destino, roque_preto = False, roque_branco = False, en_passant = False):
        """
        Move uma peça de "origem" até "destino", aplicando regras especiais (roque, en passant).

        Args:
            origem (str): posição de origem dessa peça. (Ex: "04").
            destino (str): posição final dessa peça. (Ex: "05").
            roque_preto (bool | optional): Se True, indica roque das pretas.
            roque_branco (bool | optional): Se True, indica roque das brancas.
            en_passant (bool | optional): Se True, indica movimento en passant.
        """

        peca = self.get_peca(origem)

        # Se for roque branco, verifica a posição de destino
        if roque_branco == True:
            self.posiciona_peca(peca, destino)
            self.posiciona_peca(None, origem)
            peca.posicao = destino

            # Verifica se a peça movida será um rei e atualiza a posição da rei
            if type(peca).__name__[0].lower() == "k":
                self.posicao_rei_branco = destino

                # Será um roque curto
                if destino == "76":
                    torre = self.get_peca("77")
                    self.posiciona_peca(torre, "75")
                    self.posiciona_peca(None, "77")
                    torre.posicao = "75"
                    torre.mexeu += 1
                    return 
                
                # Será um roque longo
                if destino == "72":
                    torre = self.get_peca("70")
                    self.posiciona_peca(torre, "73")
                    self.posiciona_peca(None, "70")
                    torre.posicao = "73"
                    torre.mexeu += 1
                    return 
                
        # Se for roque preto, verifica a posição de destino        
        if roque_preto == True:
            self.posiciona_peca(peca, destino)
            self.posiciona_peca(None, origem)
            peca.posicao = destino

            # Verifica se a peça movida será um rei e atualiza a posição da rei
            if type(peca).__name__[0].lower() == "k":
                self.posicao_rei_preto = destino

                # Será um roque curto
                if destino == "06":
                    torre = self.get_peca("07")
                    self.posiciona_peca(torre, "05")
                    self.posiciona_peca(None, "07")
                    torre.posicao = "05"
                    torre.mexeu += 1
                    return 
                
                # Será um roque longo
                if destino == "02":
                    torre = self.get_peca("00")
                    self.posiciona_peca(torre, "03")
                    self.posiciona_peca(None, "00")
                    torre.posicao = "03"
                    torre.mexeu += 1
                    return 
                
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
            return 
        
        # Coloca a peça na posição de destino, e o none na posição antiga da peça
        self.posiciona_peca(peca, destino)
        self.posiciona_peca(None, origem)
        peca.posicao = destino

        # Atualiza a posição do rei no atributo
        if isinstance(peca, King):
            if peca.cor == 0:
                self.posicao_rei_branco = destino
            else:
                self.posicao_rei_preto = destino

    def verificar_roque(self, cor):
        """
        Verifica se o roque (curto ou longo) é possível de ser executado.

        A verificação considera:
            - O rei está em sua posição inicial.
            - O rei e a torre correspondente nunca se moveram.
            - As casas entre rei e torre estão livres.

        Caso válido, adiciona a posição final do rei (curto ou longo) à sua 
        lista de movimentos possíveis e atualiza a flag de roque.  
    
        Args:
            cor_jogador (int): Cor do jogador a ser analisado (0 para branco, 1 para preto).
        """

        # Qual jogador deve ser verificado
        if cor == 0:

            # Se o jogador já rocou, retorna
            if self.roque_branco == 2:
                return
            
            # Pega a posição que o rei ocupa no começo do jogo, caso ele não esteja, é sinal que ele já seu moveu e não deve rocar
            rei_branco = self.copia_grid[7][4]

            # Verifica se ele está realmente nessa posição
            if rei_branco != None and type(rei_branco).__name__ == "King":

                # Verifica se ele já moveu. Ele pode andar pra frente e retornar pro mesmo lugar depois, nesse caso o roque não pode acontecer
                if rei_branco.mexeu == 0:

                    # Verifica se as posições do cavalo e do bispo estão vazias. Necessário para o roque
                    if self.copia_grid[7][5] == None and self.copia_grid[7][6] == None:

                        # Pega a torre, e faz a mesma verificação do rei
                        torre_branca_direita = self.copia_grid[7][7]
                        if torre_branca_direita != None and type(torre_branca_direita).__name__ == "Rook":
                            if torre_branca_direita.mexeu == 0:

                                # Caso tudo esteja correto, é armazenada a posição do roque e a flag é atualizada
                                rei_branco.lista_posicoes_validas.append("76")
                                self.roque_branco = 1

                    # É feita mesma verificação agora com a torre da esquerda 
                    if self.copia_grid[7][3] == None and self.copia_grid[7][2] == None and self.copia_grid[7][1] == None:
                        torre_branca_esquerda = self.copia_grid[7][0]

                        if torre_branca_esquerda != None and type(torre_branca_esquerda).__name__ == "Rook":

                            if torre_branca_esquerda.mexeu == 0:
                                rei_branco.lista_posicoes_validas.append("72")
                                self.roque_branco = 1

        # É feita a mesma verificação das brancas, agora com as pretas
        if cor == 1:
            if self.roque_preto == 2:
                return
            

            rei_preto = self.copia_grid[0][4]
            if rei_preto != None and type(rei_preto).__name__ == "King":
                if rei_preto.mexeu == 0:

                    if self.copia_grid[0][5] == None and self.copia_grid[0][6] == None:
                        torre_preta_direita = self.copia_grid[0][7]

                        if torre_preta_direita != None and type(torre_preta_direita).__name__ == "Rook":

                            if torre_preta_direita.mexeu == 0:
                                rei_preto.lista_posicoes_validas.append("06")
                                self.roque_preto = 1

                    if self.copia_grid[0][3] == None and self.copia_grid[0][2] == None and self.copia_grid[0][1] == None:
                        torre_preta_esquerda = self.copia_grid[0][0]

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
        cor = 1 - cor_peao    

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
        direcao = -1 if cor == 0 else 1

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
                peao_lateral = self.get_peca(posicao_lateral)

                # Verifica se realmente é um peão, e se ele pertence ao jogador adversário (aquele que irá fazer o en passant)
                if (peao_lateral != None and isinstance(peao_lateral, Pawn) and peao_lateral.cor == cor):

                    # Caso sim, é armazenada nas posições válidas do peão e a flag atualiza permitindo o en passant
                    posicao_en_passant = str(linha_destino + direcao) + str(coluna_destino)
                    peao_lateral.lista_posicoes_validas.append(posicao_en_passant)
                    self.en_passant = 1
    
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
        
        # É guardada essa jogada no histórico e contabiliza-se mais um para o turno
        self.historico.append(movimento)
        self.turno += 1

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
    
    def promover_peao(self):
        """
        Promove o peão na posição indicada por `self.promover_posicao` para uma rainha automaticamente.
        """

        # Pega-se a posição do peão através do "promover_posicao"
        peao = self.get_peca(self.promover_posicao)

        # Caso não haja um peão, ou for None, retorna
        if peao == None or type(peao).__name__ != "Pawn":
            return
        
        # É posicionada uma rainha no lugar atual desse peão
        self.posiciona_peca(Queen(self.cor, self.promover_posicao), self.promover_posicao)

        # Salva o histórico com a promoção
        self.salvar_historico("P", "b" if self.cor == 0 else "p", self.promover_posicao, self.promover_posicao, promocao = True, peca_promovida = "Q")

    def esta_em_mate_ou_afogamento(self, cor):
        """
        Verifica se o jogador da cor especificada está em xeque-mate ou afogamento (impasse).

        Args:
            cor (int): Cor do jogador (0 para branco, 1 para preto).

        Returns:
            str | None: "MATE" se é xeque-mate, "AFOGAMENTO" se é empate por afogamento,
            ou None caso não seja nenhuma dessas possibilidades.
        """

        # Lista para conter todos movimentos possíveis
        movimentos_possiveis = []

        # Vasculha todo o tabuleiro em busca das peças
        for i in range(8):
            for j in range(8):
                peca = self.copia_grid[i][j]

                # Se for uma peça do jogador analisado
                if peca and peca.cor == cor:

                    # Através da origem e da cor, é calculado os movimentos da peça
                    origem = f"{i}{j}"
                    destinos = self.calcular_movimento(origem, cor)

                    # Os movimentos calculados são adicionados na lista de movimentos possíveis
                    movimentos_possiveis.extend(destinos)

        # Caso a lista esteja vazia            
        if not movimentos_possiveis:

            # Se ela estiver vazia e o rei estiver em xeque, significa que foi um xeque-mate
            if (cor == 0 and self.rei_branco_check) or (cor == 1 and self.rei_preto_check):
                return "MATE"
            
            # Caso não seja um xeque, será empate por afogamento
            else:
                return "AFOGAMENTO"
            
        return None

############################################################################################################################################################
############################################################################################################################################################
# Imports necessários
import random
import os
import pickle

class QLearning:
    """
    Classe QLearning.

    Implementa um agente de IA para Xadrez utlizando o algoritmo Q-Learning.

    Através de valores Q, ela atualiza e armazena diferentes estados do tabuleiro, 
    combinando aprendizagem por reforço e heurísticas para escolher a jogada mais
    vantajosa de cada situação.
    """

    def __init__(self, jogo, alpha = 0.1, gamma = 0.9, epsilon = 0.5):
        """
        Inicializa o QLearning com seus principais atributos.

        Args:
            jogo (Game): Instância da classe Game, representando o estado atual do tabuleiro.
            alpha (int | optional): Taxa de aprendizado. Padrão: 0.1.
            gamma (int | optional): Fator de desconto para recompensas futuras. Padrão: 0.9.
            epsilon (int | optional): Taxa de exploração, a probabilidade de escolher uma jogada aleatória. Padrão: 0.5.
        """

        # Inicialização dos atributos
        self.q_table = {}
        self.jogo = jogo
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

        # Carregamento da q-table
        self.q_table = self.carregar_q_table()

    def contar_pecas(self, tabuleiro, cor):
        """
        Conta quantas peças totais um determinado jogador estão no tabuleiro.

        Args:
            tabuleiro (list[list[Piece | None]]): Lista aninhada que representa o tabuleiro.
            cor (int): Cor do jogador (0 = Branco, 1 = Preto).

        Returns:
            int: Quantidade de peças que o jogador ainda possui.
        """

        return sum(1 for p in tabuleiro if p["cor"] == cor)

    def escolher_acao(self, estado, acoes_possiveis, forcar_melhor = False):
        """
        Escolhe uma ação usando a política epsilon-greedy baseada no Q-Table.

        Args:
            estado (string): Representação única do estado atual do tabuleiro.
            acoes_possiveis (list): Lista de possíveis movimentos.
            forcar_melhor (bool | optional): Se True, sempre escolhe a melhor ação conhecida, ignorando exploração. Padrão: False.

        Return:
            any: Ação escolhida a partir de 'acoes_possiveis', ou None, caso não haja ações possíveis.
        """

        # Se a lista de acoes_possiveis estiver vaga, retorna None
        if not acoes_possiveis:
            return None

        # Escolhe aleatória baseada em epsilon caso a flag seja falsa
        if not forcar_melhor and random.random() < self.epsilon:
            return random.choice(acoes_possiveis)

        # Se o estado não existir na Q-table, inicializa com valor 0 para todas as ações possíveis
        if estado not in self.q_table:
            self.q_table[estado] = {acao: 0 for acao in acoes_possiveis}

        # Obtém os valores Q das ações possíveis para este estado
        acoes_q = {acao: self.q_table[estado].get(acao, 0) for acao in acoes_possiveis}

        # Encontra o maior valor Q e filtra apenas as ações que possuem esse valor
        max_valor = max(acoes_q.values())
        melhores_acoes = [acao for acao, valor in acoes_q.items() if valor == max_valor]

        # Retorna aleatóriamente uma entre as melhores ações
        return random.choice(melhores_acoes)

    def atualizar(self, estado, acao, recompensa, proximo_estado, acoes_proximas):
        """
        Atualiza a Q-Table aplicando a fórmula do Q-Learning para o estado e ação atual.

        Args:
            estado (str): Representação do estado do tabuleiro.
            acao (str): Ação realizada no formato "xyxy" (Ex: "0406").
            recompensa (float): Valor da recompensa obtida após realizar a ação.
            proximo_estado (str): Representação nova do estado do tabuleiro após realizar a ação.
            acoes_proximas (list): Lista de ações possíveis a partir do próximo estado.
        """

        # Garante que o estado atual e a ação existam no Q-Table
        self.q_table.setdefault(estado, {})
        self.q_table[estado].setdefault(acao, 0)

        # Garante que o próximo estado e a ação estejam presentes no Q-Table
        self.q_table.setdefault(proximo_estado, {})
        for a in acoes_proximas:
            self.q_table[proximo_estado].setdefault(a, 0)

        # Obtém o maior valor Q entre as ações do próximo estado
        max_q_proximo = max(
            [self.q_table[proximo_estado].get(a, 0) for a in acoes_proximas],
            default=0
        )

        # Fórmula do Q-Learning
        # Q(s, a) <- Q(s, a) + a * (recompensa + y * maxQ(s', a') - Q(s, a))
        q_antigo = self.q_table[estado][acao]
        novo_valor = q_antigo + self.alpha * (recompensa + self.gamma * max_q_proximo - q_antigo)
        self.q_table[estado][acao] = novo_valor
        
    def gerar_estado(self, ia, tabuleiro, cor_ia):
        """
        Gera uma tupla representando o estado atual do tabuleiro para uso no Q-Learning.

        Args:
            ia (IA): Instância da classe IA.
            tabuleiro (list): Lista aninhada 8x8 com as peças do jogo (None ou as instâncias das peças)
            cor_ia (int): Cor da IA nessa partida (0 = branco, 1 = preto).

        Returns:
            tuple: Estado do tabuleiro no formato:
                (material, xeque, mobilidade, centro, roque_rei, roque_torre_esquerda, roque_torre_direita).
        """

        # Calcula o material da IA
        material = self.calcular_material(tabuleiro, cor_ia)

        # Indica se o adversário está em xeque
        xeque = int(self.jogo.rei_preto_check if cor_ia == 1 else self.jogo.rei_branco_check)

        # Conta a quantidade de movimentos disponíveis para a IA
        mobilidade = self.contar_movimentos_validos(ia, cor_ia, tabuleiro)

        # Soma pontos por peças posicionadas no centro do tabuleiro
        centro = self.pontos_centro(tabuleiro, cor_ia, tabuleiro_notacao_normal = True)
        
        rei = None
        torre_esquerda = None
        torre_direita = None

        # Vasculha todo o tabuleiro em busca do rei e das torres da IA
        for i in range(8):
            for j in range(8):
                peca = tabuleiro[i][j]
                if peca:
                    if type(peca).__name__ == "Rei" and peca.cor == cor_ia:
                        rei = peca
                    elif type(peca).__name__ == "Torre" and peca.cor == cor_ia:
                        if j == 0:
                            torre_esquerda = peca
                        elif j == 7:
                            torre_direita = peca

        # Confere se é possível realizar o Xeque
        roque_rei = 0 if not rei or rei.mexeu else 1
        roque_torre_esquerda = 0 if not torre_esquerda or torre_esquerda.mexeu else 1
        roque_torre_direita = 0 if not torre_direita or torre_direita.mexeu else 1

        return (material, xeque, mobilidade, centro, roque_rei, roque_torre_esquerda, roque_torre_direita)
       
    def calcular_recompensa(self, ia, tabuleiro_anterior, tabuleiro_atual):
        """
        Calcula a recompensa gerada por um movimento da IA, 
        baseada em heurística.

        A função avalia o tabuleiro antes e depois da jogada, atribuindo pontos,
        positivos ou negativos conforme ganhos materiais, movimentos especiais,
        desenvolvimento de peças e condições de fim de jogo.

        Args:
            ia (IA): Instância da classe IA.
            tabuleiro_anterior (list[list[Piece | None]]): Estado do tabuleiro antes de realizar o movimento.
            tabuleiro_atual (list[list[Piece | None]]): Estado do tabuleiro após ser realizado o movimento.

        Returns:
            float: Valor númerico da recompensa (negativo ou positivo).
        """

        # São avaliados os dois estados do tabuleiro separadamente (antes e depois) e depois calcula a diferença
        pontos_antes = self.avaliar_tabuleiro(tabuleiro_anterior, ia.cor)
        pontos_depois = self.avaliar_tabuleiro(tabuleiro_atual, ia.cor)
        recompensa = pontos_depois - pontos_antes

        # Caso a jogada seja neutra, é penalizado
        if recompensa == 0:
            recompensa -= 0.3

        # Conta a quantidade de peças inimigas antes e depois do movimento
        inimigo = 1 - ia.cor
        capturas_antes = self.contar_pecas(tabuleiro_anterior, inimigo)
        capturas_depois = self.contar_pecas(tabuleiro_atual, inimigo)

        # Bonifica capturas de peças inimigas
        if capturas_depois < capturas_antes:
            recompensa += 50  

        # Analisa a última jogada, para identificar movimentos especiais e atribuir bônus por eles
        ultima_jogada = ia.historico[-1] if ia.historico else ""
        if "r" in ultima_jogada:
            recompensa += 40 
        if "e" in ultima_jogada: 
            recompensa += 10  
        if "p" in ultima_jogada: 
            recompensa += 30 
        if "C" in ultima_jogada:
            recompensa += 50 
        if ia.rei_branco_check and ia.cor == 1: 
            recompensa += 15
        if ia.rei_preto_check and ia.cor == 0:  
            recompensa += 15

        # Verifica se a posição leva ao fim do jogo, e bonifica ou penaliza de acordo
        estado_final = ia.esta_em_mate_ou_afogamento(1 - ia.cor)
        if estado_final == "MATE":
            recompensa += 9999
        elif estado_final == "AFOGAMENTO":
            recompensa -= 100
        elif ia.esta_em_mate_ou_afogamento(ia.cor) == "MATE":
            recompensa -= 9999 

        # Caso a nova jogada abrir margem para mais desenvolvimento, é bonificado, ou penalizado de acordo
        movs_antes = self.contar_movimentos_validos(ia, ia.cor, tabuleiro_anterior)
        movs_depois = self.contar_movimentos_validos(ia, ia.cor, tabuleiro_atual)
        recompensa += (movs_depois - movs_antes) * 0.2

        # Bonifica maior controle das casas centrais
        recompensa += (self.pontos_centro(tabuleiro_atual, ia.cor, tabuleiro_notacao_normal = False) -
               self.pontos_centro(tabuleiro_anterior, ia.cor, tabuleiro_notacao_normal = False))

        return recompensa
    
    def calcular_material(self, tabuleiro, cor_ia): 
        """
        Calcula o valor do material relativo que a IA possui, 
        levando em consideração o material do oponente.

        Cada peça recebe um valor fixo e o saldo é calculado como a diferença do,
        valor das peças da IA, menos, o valor das peças do oponente.

        Args:
            tabuleiro (list): Lista aninhada do tabuleiro.
            cor_ia (int): Cor do jogador (0 = branco, 1 = preto).

        Returns:
            int: Valor material relativo.
        """

        # Definição do valor simples das peças
        valor_pecas = {
            "K": 0,
            "Q": 9,
            "R": 5,
            "B": 3,
            "H": 3,
            "P": 1
        }
        material = 0

        # Vasculha todo o tabuleiro em busca das peças
        for i in range(8):
            for j in range(8):
                peca = tabuleiro[i][j]
                if peca:
                    letra = type(peca).__name__[0].upper()
                    valor = valor_pecas.get(letra, 0)
                    
                    # Se a peça pertencer a IA é somado, se pertencer ao jogador, é diminuido
                    if peca.cor == cor_ia:
                        material += valor
                    else:
                        material -= valor
        return material

    def salvar_q_table(self, nome = "save/q_table.pkl"):
        """
        Salva o estado atual da Q-Table em um arquivo.

        Args:
            nome (str | optional): Localização do arquivo. Padrão é: "save/q_table.pkl".
        """

        os.makedirs(os.path.dirname(nome), exist_ok = True)
        with open(nome, 'wb') as f:
            pickle.dump(self.q_table, f)
        print(f"[Q-TABLE SALVA] Total de estados: {len(self.q_table)}")

    def carregar_q_table(self, nome = "save/q_table.pkl"):
        """
        Carrega uma Q-Table salva de um arquivo.

        Args:   
            nome (str | optional): Localização do arquivo. Padrão é: "save/q_table.pkl".

        Returns:
            dict: Q-Table carregada. Retorna um dicionário vazio, se o arquivo não existir.
        """

        if os.path.exists(nome):
            with open(nome, 'rb') as f:
                return pickle.load(f)
        return {}
    
    def avaliar_tabuleiro(self, tabuleiro, cor_ia):
        """
        Avalia o estado do tabuleiro usando uma heurística baseado
        no valor de peças, posição e mobilidade.

        A função calcula um valor númerico que representa a vantagem ou desvantagem para a IA.

        Args:
            tabuleiro (list[dict]): Lista de dicionários, contendo as peças, e as suas posições.
                Cada dicionário contem as chaves: "letra", "cor", "x", "y".
            cor_ia (int): Representa a cor da ia (0 = branco, 1 = preto).

        Returns:
            int: Valor heurístico do tabuleiro para a IA. Valores positivos indicam 
            vantagem, negativos, desvantagem.
        """

        # Verifica se o rei ainda existe no tabuleiro, caso não, retorna imediatamente com valor extramamente negativo
        rei_presente = any(p["letra"] == "K" and p["cor"] == cor_ia for p in tabuleiro)
        if not rei_presente:
            return -99999

        # Definição do valor simples das peças
        valor_pecas = {
            "K": 10000,
            "Q": 900,
            "R": 500,
            "B": 330,
            "H": 320,
            "P": 100
        }
        pontos = 0

        # Avaliação do material, progresso e controle de centro
        for peca in tabuleiro:
            letra = peca["letra"]
            cor = peca["cor"]
            x = peca["x"]
            y = peca["y"]
            valor = valor_pecas.get(letra, 0)

            # Se a peça for da IA é somado, caso seja do adversário, é diminuido
            if cor == cor_ia:
                pontos += valor
            else:
                pontos -= valor

            # Valor adicional para peões avançados
            if letra == "P":
                if cor == cor_ia:
                    pontos += (7 - x) * 20
                else:
                    pontos -= x * 20

            # Bônus para peças no centro 
            if (x, y) in [(3, 3), (3, 4), (4, 3), (4, 4)]:
                if cor == cor_ia:
                    pontos += 200
                else:
                    pontos -= 200

        # Mobilidade: soma de movimentos possíveis
        movimentos = 0
        for i in range(8):
            for j in range(8):
                peca = self.jogo.tabuleiro.get_peca(f"{i}{j}")

                # Se a peça pertencer a IA, é calculado a quantidade de movimentos possíveis para essa peça
                if peca and peca.cor == cor_ia:
                    moves = len(peca.lista_posicoes_validas) if hasattr(peca, 'lista_posicoes_validas') else 0
                    movimentos += moves

        # Essa quantidade é somado no valor (valoriza desenvolver peças, e possuir mais possibilidades de respostas)
        pontos += movimentos * 2  

        return pontos
        
    def contar_movimentos_validos(self, ia, cor, tabuleiro):
        """
        Conta o número total de movimentos válidos para uma cor no tabuleiro.

        A função reconstroi o tabuleiro se necessário, a partir de uma lista de
        dicionários, e calcula quantos movimentos cada peça pode executar.

        Args:
            ia (IA): Instância da classe IA.
            cor (int): Cor das peças a serem analisadas (0 = branco, 1 = preto).
            tabuleiro (list[dict] | list[list]): Representação do tabuleiro.
                Pode ser:
                    Lista de dicionários, com as chaves "x" e "y".
                    Matriz 8x8 contendo os objetos das peças, ou None.

        Returns:
            int: Quantidade total de movimentos possíveis para a cor analisada.
        """

        # Reconstrução do tabuleiro caso ele venha como list[dict]
        if isinstance(tabuleiro, list) and tabuleiro != None and isinstance(tabuleiro[0], dict):
            grid = [[None for _ in range(8)] for _ in range(8)]
            for p in tabuleiro:
                grid[p["x"]][p["y"]] = ia.get_peca(f"{p['x']}{p['y']}")

        # Caso não seja, então é só admitir, assumindo que está no formato certo
        else:
            grid = tabuleiro 

        # Contador
        cont = 0

        # Vasculha o tabuleiro e calcula o movimento de todas as peças, atribuindo a totalidade deles ao contador
        for i in range(8):
            for j in range(8):
                peca = grid[i][j]
                if peca and peca.cor == cor: 
                    origem = f"{i}{j}"
                    moveset = ia.calcular_movimento(origem, cor)
                    cont += len(moveset)
                    
        return cont   
        
    def pontos_centro(self, tabuleiro, cor, tabuleiro_notacao_normal):
        """
        Calcula a pontuação baseada no controle das casas centrais do tabuleiro.

        O controle do centro é definido como a ocupação de casas específicas que influenciam o jogo.

        Args:
            tabuleiro (list[dict] | list[list]): Representação do tabuleiro.
                Pode ser:
                    Lista de dicionários, com as chaves "x" e "y".
                    Matriz 8x8 contendo os objetos das peças, ou None.
            cor (int): Cor das peças a serem analisadas (0 = branco, 1 = preto).
            tabuleiro_notacao_normal (bool): 
                - True: o tabuleiro é passado como matriz 8x8 (notação interna do Game e da IA).
                - False: o tabuleiro é passado como lista aninhada de dicionários.

        Returns:
            int: O total de pontos, recebidos pelo controle do centro.
        """

        # Definição do centro
        centro = {(3, 3), (3, 4), (4, 3), (4, 4), (3, 2), (4, 2), (3, 5), (4, 5)}
        pontos = 0

        # Verifica se a notação enviada é a normal
        if tabuleiro_notacao_normal == True:

            # Tabuleiro como matriz 8x8
            # Vasculha a lista em busca das peças
            for p in tabuleiro:
                for peca in p:
                    if peca != None:

                        # Verifica se a posição dessa peça está no centro
                        if peca.posicao in centro:

                            # Caso seja uma peça da IA, é somado, se for do adversário, é diminuido
                            pontos += 5 if p["cor"] == cor else -5
        
        # Se pertencer à outra notação
        else:

            # Tabuleiro como lista de dicionários
            # Analisa os dicionários das peças, e se suas posições estão no centro
            for p in tabuleiro:
                if (p["x"], p["y"]) in centro:

                    # Caso seja uma peça da IA, é somado, se for do adversário, é diminuido
                    pontos += 5 if p["cor"] == cor else -5

        return pontos