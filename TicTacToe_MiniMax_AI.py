# -*- coding: utf-8 -*-
"""TDE02 IA.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1TGZYAZ9Lp8rmYE1GjT_LaNLpgN0nxbWE

Alunos:

1.   Cauã Oliveira Gregorio  
2.   Eduardo Pavelecini Belleboni
3.   Franklin Jeronimo Belasque Bauch Vieira
4.   João Pedro Aires de Siqueira
5.   Laura Hundzinski da Rocha
"""

import random
import time

# Definindo o tabuleiro 4x4
class Tabuleiro:
    def __init__(self):
        self.board = [[' ' for _ in range(4)] for _ in range(4)]

    def print_tabuleiro(self):
        for linha in self.board:
            print('|'.join(linha))
            print('-' * 7)

    def fazer_jogada(self, linha, coluna, simbolo):
        if self.board[linha][coluna] == ' ':
            self.board[linha][coluna] = simbolo
            return True
        return False

    def checar_vitoria(self, simbolo):
        # verificar horizontais, verticais e diagonais
        for i in range(4):
            if all([self.board[i][j] == simbolo for j in range(4)]):  # Horizontais
                return True
            if all([self.board[j][i] == simbolo for j in range(4)]):  # Verticais
                return True
        # Diagonais
        if all([self.board[i][i] == simbolo for i in range(4)]) or all([self.board[i][3 - i] == simbolo for i in range(4)]):
            return True
        return False

    def tabuleiro_cheio(self):
        return all([self.board[i][j] != ' ' for i in range(4) for j in range(4)])


# Agentes
class AgenteAleatorio:
    def __init__(self, simbolo):
        self.simbolo = simbolo

    def jogar(self, tabuleiro):
        posicoes_disponiveis = [(i, j) for i in range(4) for j in range(4) if tabuleiro.board[i][j] == ' ']
        if posicoes_disponiveis:
            linha, coluna = random.choice(posicoes_disponiveis)
            tabuleiro.fazer_jogada(linha, coluna, self.simbolo)


class AgenteMinimax:
    def __init__(self, simbolo, profundidade_maxima=3):
        self.simbolo = simbolo  # X ou O
        self.oponente = 'O' if simbolo == 'X' else 'X'
        self.profundidade_maxima = profundidade_maxima

    def heuristica(self, tabuleiro, simbolo):
        linhas = tabuleiro.board
        colunas = [[tabuleiro.board[i][j] for i in range(4)] for j in range(4)]
        diagonais = [
            [tabuleiro.board[i][i] for i in range(4)],
            [tabuleiro.board[i][3-i] for i in range(4)]
        ]

        todas_as_linhas = linhas + colunas + diagonais
        score = 0

        for linha in todas_as_linhas:
            score += self.avaliar_linha(linha, simbolo)

        return score

    def avaliar_linha(self, linha, simbolo):
        adversario = 'O' if simbolo == 'X' else 'X'
        count_simbolo = linha.count(simbolo)
        count_adversario = linha.count(adversario)
        count_vazio = linha.count(' ')

        if count_simbolo == 4:
            return 10000  # vitoria garantida
        elif count_adversario == 4:
            return -10000  # perda garantida
        elif count_simbolo == 3 and count_vazio == 1:
            return 1000  # jogada de vitoria iminente
        elif count_adversario == 3 and count_vazio == 1:
            return -1000  # bloqueio imediato
        elif count_simbolo == 2 and count_vazio == 2:
            return 100  # bom progresso
        elif count_adversario == 2 and count_vazio == 2:
            return -100  # prevenir progresso
        elif count_simbolo == 1 and count_vazio == 3:
            return 10  # jogada inicial
        elif count_adversario == 1 and count_vazio == 3:
            return -10  # prevenir adversário
        return 0

    def minimax(self, tabuleiro, profundidade, maximizando):
        vencedor = self.checar_vitoria(tabuleiro)
        if vencedor == self.simbolo:
            return 10000 - profundidade
        elif vencedor == self.oponente:
            return profundidade - 10000
        elif tabuleiro.tabuleiro_cheio():
            return 0

        if profundidade == self.profundidade_maxima:
            return self.heuristica(tabuleiro, self.simbolo if maximizando else self.oponente)

        if maximizando:
            max_score = -float('inf')
            for i in range(4):
                for j in range(4):
                    if tabuleiro.board[i][j] == ' ':
                        tabuleiro.board[i][j] = self.simbolo
                        score = self.minimax(tabuleiro, profundidade + 1, False)
                        tabuleiro.board[i][j] = ' '
                        max_score = max(max_score, score)
            return max_score
        else:
            min_score = float('inf')
            for i in range(4):
                for j in range(4):
                    if tabuleiro.board[i][j] == ' ':
                        tabuleiro.board[i][j] = self.oponente
                        score = self.minimax(tabuleiro, profundidade + 1, True)
                        tabuleiro.board[i][j] = ' '
                        min_score = min(min_score, score)
            return min_score

    def checar_vitoria(self, tabuleiro):
        # checa se há um vencedor (X ou O) nas linhas, colunas ou diagonais
        simbolos = ['X', 'O']
        for simbolo in simbolos:
            if tabuleiro.checar_vitoria(simbolo):
                return simbolo
        return None

    def jogar(self, tabuleiro):
        melhor_score = -float('inf')
        melhor_movimento = None
        for i in range(4):
            for j in range(4):
                if tabuleiro.board[i][j] == ' ':
                    tabuleiro.board[i][j] = self.simbolo
                    score = self.minimax(tabuleiro, 0, False)
                    tabuleiro.board[i][j] = ' '
                    if score > melhor_score:
                        melhor_score = score
                        melhor_movimento = (i, j)

        if melhor_movimento:
            linha, coluna = melhor_movimento
            tabuleiro.fazer_jogada(linha, coluna, self.simbolo)

class AgenteMinimaxPoda:
    def __init__(self, simbolo, profundidade_maxima=3):
        self.simbolo = simbolo  # X ou O
        self.oponente = 'O' if simbolo == 'X' else 'X'
        self.profundidade_maxima = profundidade_maxima

    def heuristica(self, tabuleiro, simbolo):
        linhas = tabuleiro.board
        colunas = [[tabuleiro.board[i][j] for i in range(4)] for j in range(4)]
        diagonais = [
            [tabuleiro.board[i][i] for i in range(4)],
            [tabuleiro.board[i][3-i] for i in range(4)]
        ]

        todas_as_linhas = linhas + colunas + diagonais
        score = 0

        for linha in todas_as_linhas:
            score += self.avaliar_linha(linha, simbolo)

        return score

    def avaliar_linha(self, linha, simbolo):
        adversario = 'O' if simbolo == 'X' else 'X'
        count_simbolo = linha.count(simbolo)
        count_adversario = linha.count(adversario)
        count_vazio = linha.count(' ')

        if count_simbolo == 4:
            return 10000  # vitoria garantida
        elif count_adversario == 4:
            return -10000  # perda garantida
        elif count_simbolo == 3 and count_vazio == 1:
            return 1000  # jogada de vitoria iminente
        elif count_adversario == 3 and count_vazio == 1:
            return -1000  # bloqueio imediato
        elif count_simbolo == 2 and count_vazio == 2:
            return 100  # bom progresso
        elif count_adversario == 2 and count_vazio == 2:
            return -100  # prevenir progresso
        elif count_simbolo == 1 and count_vazio == 3:
            return 10  # jogada inicial
        elif count_adversario == 1 and count_vazio == 3:
            return -10  # prevenir adversário
        return 0

    def minimax_alfa_beta(self, tabuleiro, profundidade, maximizando, alfa, beta):
        vencedor = self.checar_vitoria_min(tabuleiro)
        if vencedor == self.simbolo:
            return 10000 - profundidade
        elif vencedor == self.oponente:
            return profundidade - 10000
        elif tabuleiro.tabuleiro_cheio():
            return 0  # Empate

        if profundidade == self.profundidade_maxima:
            return self.heuristica(tabuleiro, self.simbolo if maximizando else self.oponente)

        if maximizando:
            max_score = -float('inf')
            for i in range(4):
                for j in range(4):
                    if tabuleiro.board[i][j] == ' ':
                        tabuleiro.board[i][j] = self.simbolo
                        score = self.minimax_alfa_beta(tabuleiro, profundidade + 1, False, alfa, beta)
                        tabuleiro.board[i][j] = ' '
                        max_score = max(max_score, score)
                        alfa = max(alfa, score)
                        if beta <= alfa:
                            break  # poda beta
            return max_score
        else:
            min_score = float('inf')
            for i in range(4):
                for j in range(4):
                    if tabuleiro.board[i][j] == ' ':
                        tabuleiro.board[i][j] = self.oponente
                        score = self.minimax_alfa_beta(tabuleiro, profundidade + 1, True, alfa, beta)
                        tabuleiro.board[i][j] = ' '
                        min_score = min(min_score, score)
                        beta = min(beta, score)
                        if beta <= alfa:
                            break  # poda alfa
            return min_score

    def checar_vitoria_min(self, tabuleiro):
        # checa se há um vencedor (X ou O) nas linhas, colunas ou diagonais
        simbolos = ['X', 'O']
        for simbolo in simbolos:
            if tabuleiro.checar_vitoria(simbolo):
                return simbolo
        return None

    def jogar(self, tabuleiro):
        melhor_score = -float('inf')
        melhor_movimento = None
        alfa = -float('inf')
        beta = float('inf')
        for i in range(4):
            for j in range(4):
                if tabuleiro.board[i][j] == ' ':
                    tabuleiro.board[i][j] = self.simbolo
                    score = self.minimax_alfa_beta(tabuleiro, 0, False, alfa, beta)
                    tabuleiro.board[i][j] = ' '
                    if score > melhor_score:
                        melhor_score = score
                        melhor_movimento = (i, j)

        if melhor_movimento:
            linha, coluna = melhor_movimento
            tabuleiro.fazer_jogada(linha, coluna, self.simbolo)

# funcao para selecionar agentes
def selecionar_agente(simbolo):
    print("Selecione a estratégia do Agente:")
    print("1 - Aleatório")
    print("2 - Minimax")
    print("3 - Minimax com poda Alfa-Beta")

    escolha = int(input("Escolha a estratégia (1-3): "))
    if escolha == 1:
        return AgenteAleatorio(simbolo)
    elif escolha == 2:
        return AgenteMinimax(simbolo)
    elif escolha == 3:
        return AgenteMinimaxPoda(simbolo)  # trocar para a versão com poda alfa-beta


def jogar_jogo():
    print("Escolha o modo de jogo:")
    print("1 - Humano X Computador")
    print("2 - Computador X Computador")

    modo_de_jogo = int(input("Escolha o modo de jogo (1 ou 2): "))
    tabuleiro = Tabuleiro()

    if modo_de_jogo == 1:
        print("Configuração do Computador:")
        agente_computador = selecionar_agente('O')
        simbolo_humano = 'X'
    else:
        print("Configuração do Computador 1:")
        agente_computador1 = selecionar_agente('X')
        print("Configuração do Computador 2:")
        agente_computador2 = selecionar_agente('O')

    numero_jogada = 0
    while True:
        if modo_de_jogo == 1:
            tabuleiro.print_tabuleiro()
            while True:
              linha = int(input("Escolha a linha (0-3): "))
              if 0 <= linha <= 3:
                  break
              else:
                  print("Escolha uma linha válida.")

            while True:
              coluna = int(input("Escolha a coluna (0-3): "))
              if 0 <= coluna <= 3:
                  break
              else:
                  print("Escolha uma coluna válida.")
            if tabuleiro.fazer_jogada(linha, coluna, simbolo_humano):
                numero_jogada += 1
                if tabuleiro.checar_vitoria(simbolo_humano):
                    print("Humano venceu!")
                    break
                if tabuleiro.tabuleiro_cheio():
                    print("Empate!")
                    break
                start_time = time.time()
                agente_computador.jogar(tabuleiro)
                end_time = time.time()
                numero_jogada += 1
                print(f"Jogada {numero_jogada}, Tempo gasto: {end_time - start_time:.2f} segundos")
                if tabuleiro.checar_vitoria(agente_computador.simbolo):
                    print("Computador venceu!")
                    break
                if tabuleiro.tabuleiro_cheio():
                    print("Empate!")
                    break
        else:
            # Computador X Computador
            start_time = time.time()
            agente_computador1.jogar(tabuleiro)
            end_time = time.time()
            numero_jogada += 1
            print(f"Jogada {numero_jogada}, Tempo gasto: {end_time - start_time:.2f} segundos")
            tabuleiro.print_tabuleiro()

            if tabuleiro.checar_vitoria(agente_computador1.simbolo):
                print("Computador 1 venceu!")
                break
            if tabuleiro.tabuleiro_cheio():
                print("Empate!")
                break

            start_time = time.time()
            agente_computador2.jogar(tabuleiro)
            end_time = time.time()
            numero_jogada += 1
            print(f"Jogada {numero_jogada}, Tempo gasto: {end_time - start_time:.2f} segundos")
            tabuleiro.print_tabuleiro()

            if tabuleiro.checar_vitoria(agente_computador2.simbolo):
                print("Computador 2 venceu!")
                break
            if tabuleiro.tabuleiro_cheio():
                print("Empate!")
                break

# Executa o jogo
jogar_jogo()