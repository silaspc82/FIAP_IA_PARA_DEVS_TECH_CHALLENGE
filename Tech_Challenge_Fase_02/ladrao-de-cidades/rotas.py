import rota as rota
import random
class Rotas():
  def __init__(self, dados):
    self.tamanho = 10
    self.populacao = []
    self.dados = dados #dados do problema

    #cria a população inicial
    for i in range(self.tamanho):
      self.populacao.append(rota.Rota(dados))
 
  #retorna uma lista com os individuos mutados da população
  def mutacao(self):
    mutados = []
    for individuo in self.populacao:
      mutado = individuo.mutacao()
      mutados.append(mutado)
    return mutados

  #retorna o individuo mais adaptado da população
  def top(self):
    lista_ordenada = sorted(self.populacao, key=lambda x: x.fitness_val, reverse=True)
    return lista_ordenada[0]

  #seleciona os 10 melhores individuos da população
  def selecionar(self, populacao1, populacao2):
    populacao_total = self.populacao + populacao1 + populacao2
    lista_ordenada = sorted(populacao_total, key=lambda x: x.fitness_val, reverse=True)
    mais_adaptados = lista_ordenada[:10]
    self.populacao = mais_adaptados

  #Faz o cruzamento de duas listas
  # - Exemplo: metade 1 = [1, 2, 3, 4, 5] e metade 2 = [6, 7, 8, 9, 10]
  # - 1 cruza com 6, 2 cruza com 7, 3 cruza com 8, 4 cruza com 9 e 5 cruza com 10
  # - Resultado: [1, 7, 3, 9, 5] e [6, 2, 8, 4, 10]
  def cruzar(lista1, lista2):
      nova_lista1 = []
      nova_lista2 = []
      
      for i in range(len(lista1)):
          if i % 2 == 0:
              nova_lista1.append(lista1[i])
              nova_lista2.append(lista2[i])
          else:
              nova_lista1.append(lista2[i])
              nova_lista2.append(lista1[i])

      return nova_lista1, nova_lista2

  #Retorna uma lista com os individuos cruzados da população
  #Funciona assim:
  # 1 - Divide a população em duas metades
  # 2 - Para cada metade, cruza os individuos com os individuos da outra metade
  # 3 - Retorna a nova população
  def crossover(self):
    nova_populacao = []
    novos_individuos = []

    # 1 - Divide a população em duas metades
    tamanho_pop = len(self.populacao)
    metade = tamanho_pop // 2
    metade_1 = self.populacao[:metade]
    metade_2 = self.populacao[metade:]

    # 2 - Cruza os individuos das duas metades
    for i in range(metade):
      nova_lista1, nova_lista2 = Rotas.cruzar(metade_1[i].rota, metade_2[i].rota)
      novos_individuos.append(nova_lista1)
      novos_individuos.append(nova_lista2)

    # 3 - Gera novos individuos com as novas rotas
    for individuo in novos_individuos:
      nova_populacao.append(rota.Rota(self.dados, individuo))

    # 4 - Retorna a nova população
    return nova_populacao