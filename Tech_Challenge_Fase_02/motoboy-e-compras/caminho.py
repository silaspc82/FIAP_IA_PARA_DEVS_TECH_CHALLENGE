import tabulate
import random
from dados import Dados
from decimal import *
from exceptions import TempoDecorridoException, PesoException, SuperMercadoSemCompraException, FitValidacaoException

QTD_SUPERMERCADOS_LISTA = 8


class Caminho():
    def __init__(self, dados: Dados, caminho=None):

        self.caminho = caminho
        self.dados = dados
        self.tempo_caminho = 0
        self.peso_total = 0
        self.fit_caminho = 0
        self.status = True
        if not self.caminho:
            tentar_novamente = True
            qtd_tentativas = 50
            while tentar_novamente and qtd_tentativas > 0:
                tentar_novamente = False
                self.caminho = self.gerar_rota_super_mercado()
                try:
                    self.fitness()
                except FitValidacaoException as e:
                    tentar_novamente = True
                    qtd_tentativas -= 1

                if not self.status and not tentar_novamente:
                    tentar_novamente = True
                    qtd_tentativas -= 1
        else:
            try:
                self.fitness()
            except FitValidacaoException as e:
                pass

    def __str__(self):
        return f"Fitness caminho: {self.fit_caminho}\nStatus: {self.status}\nCaminho: {self.caminho}\nPreço produto: R$ {self.valor_total()}\nPeso produto: {self.peso_total}g\nTempo caminho: {self.tempo_caminho}min"

    def gerar_rota_super_mercado(self):
        if QTD_SUPERMERCADOS_LISTA % 2 != 0:
            raise Exception(
                "gerar_rota_super_mercado(): QTD_SUPERMERCADOS_LISTA precisa ser um número par.")
        if QTD_SUPERMERCADOS_LISTA > len(list(self.dados.lista_super_mercados.keys())):
            raise Exception(
                "gerar_rota_super_mercado(): QTD_SUPERMERCADOS_LISTA precisa ser menor que o número de supermercados existente.")

        super_mercados = list(self.dados.lista_super_mercados.keys())
        random.shuffle(super_mercados)

        return super_mercados[0:QTD_SUPERMERCADOS_LISTA]

    def mutacao(self):
        if random.random() > 0.7:
            if len(self.caminho) <= 2:
                return self

            caminho = self.caminho[:]
            indice = random.randint(0, len(caminho) - 2)
            caminho[indice], caminho[indice +
                                        1] = self.caminho[indice+1], self.caminho[indice]
            self.caminho = caminho
            try:
                self.fitness()
            except FitValidacaoException as e:
                pass
        return self

    def gerarRelatorio(self):
        super_mercados_visitados = self.caminho

        headers = ['Supermercado', 'Produto Comprado', 'Peso', 'Preço']

        tabela = []
        produtos_comprados = self.procurar_produtos_baratos_caminho()
        for super_mercado in super_mercados_visitados:
            for produto in produtos_comprados.values():
                if produto['super_mercado']['nome'] == super_mercado:
                    tabela.append(
                        [super_mercado, produto['produto']['nome'],
                            produto['produto']['peso'], produto['produto']['valor']]
                    )

        string = f"Fitness: {self.fit_caminho}\nStatus: {self.status}\nPreço total: R$ {self.valor_total()}\nPeso total: {self.peso_total}g\nTempo: {self.tempo_caminho}min\nCaminho e itens comprados:"
        print(string)
        print(tabulate.tabulate(tabela, headers=headers, tablefmt='fancy_grid'))

    def procurar_produtos_baratos_caminho(self):
        mapa_caminho_por_produto = {}
        for super_mercado in self.caminho:
            for produto_super_mercado in self.dados.lista_super_mercados[super_mercado]['produtos']:
                if produto_super_mercado['nome'] not in mapa_caminho_por_produto:
                    mapa_caminho_por_produto[produto_super_mercado['nome']] = {
                        'super_mercado': self.dados.lista_super_mercados[super_mercado], 'produto': produto_super_mercado}

                if produto_super_mercado['valor'] < mapa_caminho_por_produto[produto_super_mercado['nome']]['produto']['valor']:
                    mapa_caminho_por_produto[produto_super_mercado['nome']] = {
                        'super_mercado': self.dados.lista_super_mercados[super_mercado], 'produto': produto_super_mercado}

        return mapa_caminho_por_produto

    def valor_total(self, mapa_caminho_por_produto={}):
        if not mapa_caminho_por_produto:
            mapa_caminho_por_produto = self.procurar_produtos_baratos_caminho()

        total = Decimal(0.0)
        for produto in mapa_caminho_por_produto.values():
            total += produto['produto']['valor']
        return total

    def eficiencia(self):
        return self.calcular_tempo_total() + self.valor_total()

    def get_peso_total(self, mapa_caminho_por_produto={}):
        if not mapa_caminho_por_produto:
            mapa_caminho_por_produto = self.procurar_produtos_baratos_caminho()

        total = 0
        for produto in mapa_caminho_por_produto.values():
            total += produto['produto']['peso']

        self.peso_total = total
        return total

    def calcular_tempo_caminho(self):
        total = Decimal(0.0)

        for indice in range(0, len(self.caminho), 2):
            total += self.dados.lista_rotas_super_mercados[self.caminho[indice]
                                                           ][self.caminho[indice+1]]['tempo']

        return total

    def calcular_tempo_produto(self, mapa_caminho_por_produto={}):
        if not mapa_caminho_por_produto:
            mapa_caminho_por_produto = self.procurar_produtos_baratos_caminho()

        total = Decimal(0.0)
        for produto in mapa_caminho_por_produto.values():
            total += produto['produto']['tempo']
        return total

    def calcular_tempo_total(self):
        tempo = self.calcular_tempo_caminho() + self.calcular_tempo_produto()
        self.tempo_caminho = tempo
        return tempo

    def calcular_distancia_caminho(self, mapa_caminho_por_produto={}):
        total = Decimal(0.0)

        for indice in range(0, len(self.caminho), 2):
            total += self.dados.lista_rotas_super_mercados[self.caminho[indice]
                                                           ][self.caminho[indice+1]]['distancia']

        return total

    def identificar_super_mercado_sem_compra(self, mapa_caminho_por_produto={}):
        if not mapa_caminho_por_produto:
            mapa_caminho_por_produto = self.procurar_produtos_baratos_caminho()

        encontrou_supermercado = False
        for super_mercado in self.caminho:
            encontrou_supermercado = False
            for produto in mapa_caminho_por_produto.values():
                if super_mercado == produto['super_mercado']['nome']:
                    encontrou_supermercado = True
                    break
            if not encontrou_supermercado:
                return True

        return encontrou_supermercado

    def fitness(self):
        if self.get_peso_total() > 40000:
            self.status = False
            raise PesoException('Peso total maior que 40000')

        if self.calcular_tempo_total() > 100:
            self.status = False
            raise TempoDecorridoException('Tempo percorrido maior que 100')

        # if self.identificar_super_mercado_sem_compra():
        #     self.status = False
        #     # raise SuperMercadoSemCompraException('Supermercado sem compra encontrado.')
        #     return False

        self.status = True
        self.fit_caminho = self.eficiencia()

        return self.fit_caminho