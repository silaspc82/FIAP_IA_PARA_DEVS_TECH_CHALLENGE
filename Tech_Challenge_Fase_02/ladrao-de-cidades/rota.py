import fabrica_dados as fd
import random, tabulate

class Rota():
    def __init__(self, dados: fd.FabricaDados, rota = None):
        self.dados = dados
        self.rota = rota
        if rota == None: #se não for passada uma rota, gera uma aleatória
            self.rota = self.gerar_rota()
        self.peso = 0
        self.tempo_total = 0
        self.fitness_val = 0
        self.fitness() #calcula e atualiza o fitness_val

    def __str__(self):
        string = f"fitness: {self.fitness_val}\nstatus: {self.status}\nrota: {self.rota}\npeso: {self.peso}\ntempo: {self.tempo_total}"
        return string

    #Gera uma rota aleatória
    def gerar_rota(self):
        rota = []
        cidades = self.dados.cidades
        randon_list = random.sample(range(len(cidades)), len(cidades))
        rota.append('Escondidos')
        for i in range(13):
            rota.append(cidades[randon_list[i]])
        return rota
    

    #Muda aleatoriamente a ordem de duas cidades com exceção da primeira
    def mutacao(self):
        nova_rota = self.rota[:]
        randon_list = random.sample(range(1, len(nova_rota)), 2)
        nova_rota[randon_list[0]], nova_rota[randon_list[1]] = nova_rota[randon_list[1]], nova_rota[randon_list[0]]
        novo_individuo = Rota(self.dados, nova_rota)
        return novo_individuo #retorna um novo individuo com a rota mutada  
    
    def imprimir(self):
        cidades_visitadas = self.cria_sub_rota()
        itens_roubados = []
        valor_itens = []
        matriz_dados =[]
        
        headers = ['Cidade', 'Item roubado', 'Valor']
        
        #Adiciona o item e o valor da cidade em matriz_dados[1]
        for i in cidades_visitadas:
            itens_roubados.append(self.dados.itens[i]['item'])
            valor_itens.append(self.dados.itens[i]['valor'])
            
        for i in range(len(cidades_visitadas)):
            new_row = [cidades_visitadas[i], itens_roubados[i], f'${valor_itens[i]}']
            matriz_dados.append(new_row)
            
        string = f"Fitness: {self.fitness_val}\nStatus: {self.status}\nPeso: {self.peso}Kg\nTempo: {self.tempo_total}h\nRota e itens roubados:"
        print(string)
        print(tabulate.tabulate(matriz_dados, headers = headers, tablefmt = 'fancy_grid'))
        

    #-----------------Funções de fitness-----------------

    # Verifica se a rota é válida
    def rota_valida(self):
        # Verifica se a primeira cidade é Escondidos
        if self.rota[0] != "Escondidos":
            self.status = 'Rota inválida: a primeira cidade não é Escondidos'
            return False
        
        # Verifica se Escondidos aparece pelo menos duas vezes
        if self.rota.count('Escondidos') < 2:
            self.status = 'Rota inválida: Escondidos não aparece duas vezes'
            return False

        # Verifica se Escondidos não é a segunda cidade da rota
        if self.rota[1] == 'Escondidos':
            self.status = 'Rota inválida: Escondidos é a segunda cidade da rota'
            return False
        
        # Cria a sub-rota válida
        sub_rota = []
        i = 1
        while self.rota[i] != 'Escondidos':
            sub_rota.append(self.rota[i])
            i += 1
        
        # Verifica se a sub-rota possui cidades repetidas
        if len(sub_rota) != len(set(sub_rota)):
            self.status = 'Rota inválida: a sub-rota possui cidades repetidas'
            return False
        
        return True
    
    # Cria um array com a rota entre os dois "Escondidos"
    def cria_sub_rota(self):
        sub_rota = []
        i = 1
        while self.rota[i] != 'Escondidos':
            sub_rota.append(self.rota[i])
            i += 1
        return sub_rota

    # Retorna o valor total obtido na rota
    def valor_total(self):
        itens = self.dados.itens
        sub_rota = self.cria_sub_rota()
        valor_total = 0
        for cidade in sub_rota:
            if cidade in itens:
                valor_total += itens[cidade]['valor']
            else:
                raise Exception(f"Cidade '{cidade}' não está na lista de itens.")

        return valor_total
            
    # Retorna o tempo total da rota
    def peso_total(self):
        itens = self.dados.itens
        sub_rota = self.cria_sub_rota()
        peso_total = 0
        for cidade in sub_rota:
            if cidade in itens:
                peso_total += itens[cidade]['peso']
            else:
                raise Exception(f"Cidade '{cidade}' não está na lista de itens.")
        self.peso = peso_total
        return peso_total
    
    # Cria uma lista com a rota entre Escondidos (incluindo ambos)
    def cria_rota_efetiva(self):
        rota_efetiva = []
        i = 1
        rota_efetiva.append(self.rota[0])
        while self.rota[i] != 'Escondidos':
            rota_efetiva.append(self.rota[i])
            i += 1
        rota_efetiva.append(self.rota[i])
        
        return rota_efetiva

    # Retorna o tempo total da rota
    def calc_tempo_viagem(self):
        viagens = self.dados.viagens
        rota_efetiva = self.cria_rota_efetiva()
        tempo_total = 0
        for i in range(len(rota_efetiva)):
            if i == 0:
                continue
            else:
                try:
                    tempo_total += viagens[rota_efetiva[i-1]][rota_efetiva[i]]['tempo']
                except KeyError: 
                    raise Exception(f"Viagem entre '{rota_efetiva[i-1]}' e '{rota_efetiva[i]}' não está na lista de viagens.")
        
        return tempo_total
    
    # Retorna o tempo total de roubo da rota
    def calc_tempo_roubo(self):
        tempo_roubo = 0
        sub_rota = self.cria_sub_rota()
        for cidade in sub_rota:
            tempo_roubo += self.dados.itens[cidade]['tempo']
        return tempo_roubo
    
    # Retorna o tempo total da rota
    def calc_tempo_total(self):
        tempo = self.calc_tempo_viagem() + self.calc_tempo_roubo()
        self.tempo_total = tempo
        return tempo

    # Retorna o custo total da rota
    def calc_custo_viagem(self):
        viagens = self.dados.viagens
        rota_efetiva = self.cria_rota_efetiva()
        custo_total = 0
        for i in range(len(rota_efetiva)):
            if i == 0:
                continue
            else:
                try:
                    custo_total += viagens[rota_efetiva[i-1]][rota_efetiva[i]]['custo']
                except KeyError: 
                    raise Exception(f"Viagem entre '{rota_efetiva[i-1]}' e '{rota_efetiva[i]}' não está na lista de viagens.")
        
        return custo_total
    
    # Retorna o lucro total da rota
    def lucro(self):
        return self.valor_total() - self.calc_custo_viagem()


    def fitness(self):

        # Verifica:
        #   - Se a primeira cidade é Escondidos
        #   - Se Escondidos aparece pelo menos duas vezes
        #   - Se Escondidos não é a segunda cidade da rota
        #   - Se a rota efetiva possui cidades repetidas
        if self.rota_valida() == False:
            self.fitness_val = float('-inf')
            return float('-inf')
        
        # Verifica se o peso total da rota é maior que 20
        if self.peso_total() > 20:
            self.status = 'Inválida: Peso total maior que 20'
            self.fitness_val = float('-inf')
            return float('-inf')
        
        # Verifica se o tempo total da rota é maior que 72
        if self.calc_tempo_total() > 72:
            self.status = 'Inválida: Tempo total maior que 72'
            self.fitness_val = float('-inf')
            return float('-inf')
        
        # Retorna o valor total - custo total
        self.status = 'Fit'
        lucro = self.lucro() # Valor total - Custo total
        self.fitness_val = lucro
        return lucro