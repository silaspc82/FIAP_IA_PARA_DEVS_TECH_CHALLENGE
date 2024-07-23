import rotas as rotas, algoritmo_genetico as ag
import fabrica_dados as fd

alg_gen = ag.AlgoritmoGeneticoPopulacao(rotas.Rotas(fd.FabricaDados()))

individuo_adaptado = alg_gen.executar()

print("\nPrimeiro mais adaptado:")
print(f"Quantidade de gerações: {alg_gen.qtd_geracoes()}")
individuo_adaptado.imprimir()
alg_gen.plotar()