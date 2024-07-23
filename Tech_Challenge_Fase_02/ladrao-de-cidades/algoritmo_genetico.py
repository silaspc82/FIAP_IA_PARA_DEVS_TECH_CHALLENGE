import matplotlib.pyplot as plt

GERACOES_MAX = 25

class AlgoritmoGeneticoPopulacao:

  def __init__(self, populacao, geracoes_max=GERACOES_MAX):
    self.populacao = populacao
    self.geracoes_max = geracoes_max
    self.geracoes = 1
    self.evolucao = []

  def qtd_geracoes(self):
    return self.geracoes

  def plotar(self):
    geracoes = len(self.evolucao)
    tamanho_da_populacao = len(self.evolucao[0])

    for individuo in range(tamanho_da_populacao):
        fitness_individuo = [self.evolucao[geracao][individuo] for geracao in range(geracoes)]
        plt.scatter(range(geracoes), fitness_individuo, s=10)

    plt.xlabel('Geração')
    plt.ylabel('Fitness')
    plt.title('Fitness dos Indivíduos ao Longo das Gerações')
    plt.show()

  def executar(self):
    # Define o melhor fitness da primeira geração
    ultimo_fitness = self.populacao.top()
  
    while True:
      if self.geracoes <= self.geracoes_max:
        populacao_mutada = self.populacao.mutacao() # Mutação
        populacao_crossover = self.populacao.crossover() # Crossover
        self.populacao.selecionar(populacao_mutada, populacao_crossover)

        # for i in self.populacao.populacao:
        #   self.evolucao.append(i.fitness_val) 

        listafit = [] 
        for i in self.populacao.populacao:
          listafit.append(i.fitness_val)
        self.evolucao.append(listafit)

        fitness = self.populacao.top() # Melhor fitness da geração

        #self.evolucao.append(fitness.fitness_val) # Adiciona o fitness da geração à lista de evolução

        # Se o fitness da geração for melhor que o da última geração
        if fitness.fitness_val > ultimo_fitness.fitness_val:
          ultimo_fitness = fitness # Atualiza o melhor fitness
        self.geracoes += 1 # Incrementa o número de gerações
        if self.geracoes % 10000 == 0: # Imprime o melhor fitness a cada 10000 gerações
          print(f"Geração: {self.geracoes}\nTop fitness: \n{ultimo_fitness}\n\n")
      else:
        break
    
    return ultimo_fitness # Retorna o melhor fitness da última geração
