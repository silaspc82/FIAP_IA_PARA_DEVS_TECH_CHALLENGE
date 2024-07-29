from caminho import Caminho
import random
from exceptions import TempoDecorridoException, PopulacaoInexistenteException
import sys


class Caminhos():
    def __init__(self, dados):
        self.quantidade_supermercados_caminho = 10
        self.dados = dados
        self.populacao = []

        # TODO: Preparar o código para o hotstart

        for i in range(self.quantidade_supermercados_caminho):
            self.populacao.append(Caminho(dados))

    def mutacao(self):
        mutacoes = []
        for caminho in self.populacao:
            mutacoes.append(caminho.mutacao())
        return mutacoes

    def top(self):
        if not self.populacao:
            raise PopulacaoInexistenteException("top(): População vazia. Execute novamente!")
        
        populacao_ativa = [caminho for caminho in self.populacao if (caminho.status)]

        if not populacao_ativa:
            raise PopulacaoInexistenteException("top(): População ativa vazia. Execute novamente!")

        return sorted(populacao_ativa, key=lambda cmn: cmn.fit_caminho, reverse=True)[0]

    def selecionar(self, populacao_a, populacao_b):
        total_pop = self.populacao + populacao_a + populacao_b

        
        populacao_ativa = [caminho for caminho in total_pop if (caminho.status)]

        if not populacao_ativa:
            raise PopulacaoInexistenteException("selecionar(): População ativa vazia. Execute novamente!")

        self.populacao = sorted(
            populacao_ativa, key=lambda cmn: cmn.fit_caminho, reverse=True)[:10]

    def cruzar(parente1, parente2):
        filho_1 = None
        filho_2 = None

        if len(parente1.caminho) != len(parente2.caminho):
            raise Exception('Cruzar: Lista com tamanhos diferentes.')

        tamanho_lista = len(parente1.caminho)
        indice_inicial = random.randint(0, tamanho_lista - 1)
        indice_final = random.randint(indice_inicial+1, tamanho_lista)

        filho_1 = [None] * tamanho_lista
        filho_2 = [None] * tamanho_lista

        for i in range(indice_inicial, indice_final):
            filho_1[i] = parente1.caminho[i]
            filho_2[i] = parente2.caminho[i]

        for i in range(0, tamanho_lista):
            if i <= indice_inicial or i >= indice_final:
                for super_mercado in parente1.caminho:
                    if super_mercado not in filho_2:
                        filho_2[i] = super_mercado
                        break

                for super_mercado in parente2.caminho:
                    if super_mercado not in filho_1:
                        filho_1[i] = super_mercado
                        break

        return filho_1, filho_2

    def crossover(self):
        populacao_2 = []

        divisor_populacao = len(self.populacao) // 2

        for i in range(0, divisor_populacao):
            filhos = Caminhos.cruzar(
                self.populacao[i], self.populacao[i+divisor_populacao])
            populacao_2.append(Caminho(self.dados, filhos[0]))
            populacao_2.append(Caminho(self.dados, filhos[1]))
        return populacao_2
