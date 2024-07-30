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
        self.lista_geracao = []

    def qtd_geracao(self):
        return self.geracao

    def qtd_evolucao(self):
        return len(self.evolucao)

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

                # self.evolucao += self.populacao.populacao

                novo_melhor_caminho = self.populacao.top()

                if novo_melhor_caminho.fit_caminho < melhor_caminho_anterior.fit_caminho:
                    melhor_caminho_anterior = novo_melhor_caminho

                self.geracao += 1
                # print(f'self.geracao {self.geracao} - melhor_caminho_anterior.fit_caminho {melhor_caminho_anterior.fit_caminho}')

                self.evolucao += [melhor_caminho_anterior]
                self.lista_geracao += [self.geracao]

                

                if self.geracao % 50 == 0:
                    print(f"Geração: {self.geracao}\nFit: \n{melhor_caminho_anterior}\n\n")

        return melhor_caminho_anterior

    def gerarGrafico(self):
        fitness_individuo = [caminho.fit_caminho for caminho in self.evolucao if caminho.status]
        plotar_grafico(x=self.lista_geracao, y=fitness_individuo, x_label='Gerações', y_label='Fitness')