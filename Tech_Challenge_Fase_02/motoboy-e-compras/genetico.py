from exceptions import PopulacaoInexistenteException
import sys
import matplotlib.pyplot as plt
from gera_grafico import plotar_grafico

GERACOES_MAXIMAS = 100
class Genetico:

    def __init__(self, populacao, geracoes_maximas=GERACOES_MAXIMAS):
        self.populacao = populacao
        self.geracao = 0
        self.geracoes_maximas = geracoes_maximas
        self.evolucao = []

    def qtd_geracao(self):
        return self.geracao

    def executar(self):
        melhor_caminho_anterior = None
        try:
            melhor_caminho_anterior = self.populacao.top()
        except PopulacaoInexistenteException as e:
            print(e)
            sys.exit()

        while True:
            if self.geracao >= self.geracoes_maximas:
                break
            else:
                mutacao_populacional = self.populacao.mutacao()

                crossover_populacional = self.populacao.crossover()

                self.populacao.selecionar(
                    mutacao_populacional, crossover_populacional)

                self.evolucao += self.populacao.populacao

                novo_melhor_caminho = self.populacao.top()

                if novo_melhor_caminho.fit_caminho < melhor_caminho_anterior.fit_caminho:
                    melhor_caminho_anterior = novo_melhor_caminho

                self.geracao += 1

                if self.geracao % 50 == 0:
                    print(f"Geração: {self.geracao}\nFit: \n{melhor_caminho_anterior}\n\n")

        return melhor_caminho_anterior

    def gerarGrafico(self):
        geracoes = len(self.evolucao)

        fitness_individuo = [self.evolucao[geracao].fit_caminho for geracao in range(geracoes)]

        plotar_grafico(x=range(1, geracoes+1), y=fitness_individuo, x_label='Gerações', y_label='Fitness')