from genetico import Genetico
from caminhos import Caminhos
from dados import Dados

geneticos = Genetico(Caminhos(Dados()))

melhor_caminho = geneticos.executar()

print("\nMelhor caminho:")
print(f"Gerações: {geneticos.qtd_evolucao()}")
melhor_caminho.gerarRelatorio()
geneticos.gerarGrafico()