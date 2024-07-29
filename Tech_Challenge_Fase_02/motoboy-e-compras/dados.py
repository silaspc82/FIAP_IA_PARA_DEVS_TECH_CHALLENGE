import os
from decimal import *
import csv

class Dados:
    #Descomentar para DEBUG no ambiente local
    # debugPath = f'{os.getcwd()}/Tech_Challenge_Fase_02/motoboy-e-compras'
    # debugPath = f'{os.getcwd()}/motoboy-e-compras'
    debugPath = f'{os.getcwd()}'

    def __init__(self):
        self.lista_rotas_super_mercados = self.gerar_rotas_super_mercados()
        self.lista_super_mercados = self.gerar_lista_super_mercados()
        self.gerar_lista_produtos()

    def gerar_rotas_super_mercados(self):
        rotas = {}

        with open(f'{self.debugPath}/super_mercados.csv', encoding='utf-8') as arquivo:
            for colunas in csv.reader(arquivo):
                supermercado_origem = colunas[0]
                supermercado_destino = colunas[1]
                tempo = Decimal(colunas[2])
                distancia = Decimal(colunas[3])

                if supermercado_origem not in rotas:
                    rotas[supermercado_origem] = {}
                rotas[supermercado_origem][supermercado_destino] = {'tempo': tempo, 'distancia': distancia}

                if supermercado_destino not in rotas:
                    rotas[supermercado_destino] = {}
                rotas[supermercado_destino][supermercado_origem] = {'tempo': tempo, 'distancia': distancia}
        
        return rotas

    def gerar_lista_super_mercados(self):
        mapa_supermercados = {}
        for super_mercado in self.lista_rotas_super_mercados.keys():
            mapa_supermercados[super_mercado] = {'nome': super_mercado,'produtos': []}

        return mapa_supermercados

    def gerar_lista_produtos(self):
        with open(f'{self.debugPath}/produtos.csv', encoding='utf-8') as arquivo:
            for colunas in csv.reader(arquivo):
                nome = colunas[0]
                peso = Decimal(colunas[1])
                tempo = int(colunas[2])
                valor = Decimal(colunas[3])
                super_mercado = colunas[4]

                if super_mercado in self.lista_super_mercados:
                    self.lista_super_mercados[super_mercado]['produtos'].append({'nome': nome, 'peso': peso, 'tempo': tempo, 'valor': valor})
                else:
                    raise Exception(f'Mercado não encontrado: {super_mercado}')
