import random

taxa_cruzamento = .7
taxa_mutacao = .05

class AG_real_coded:
    populacao = dict()
    
    def __init__(self, taxa_cruzamento, taxa_mutacao, tam_pop, alelos_ul, alelos_bl, tam_cromossomo, func_avaliacao):
        self.taxa_cruzamento = taxa_cruzamento
        self.taxa_mutacao = taxa_mutacao
        self.tam_pop = tam_pop
        self.alelos_ul = alelos_ul # limite superior para os possíveis valores dos genes
        self.alelos_bl = alelos_bl # limite inferior para os possíveis valores dos genes
        self.tam_cromossomo = tam_cromossomo
        self.func_avaliacao = func_avaliacao # função de avaliação dinâmica

    def gerar_populacao_inicial(self):
        for i in range(self.tam_pop):
            cromossomo = []
            for j in range(self.tam_cromossomo):
                cromossomo.append(random.uniform(self.alelos_bl, self.alelos_ul)) # adição aleatória de genes no cromossomo (pode ter valores repetidos)

            cromossomo = tuple(cromossomo)    
            self.populacao[cromossomo] = self.avaliar_cromossomo(cromossomo)

    def cruzar(self, crom1, crom2, ponto_cruzamento):
        print("Pais: {} e {}".format(crom1, crom2))
        
        filho1 = []
        filho2 = []

        filho1.extend(crom1[0:ponto_cruzamento+1])
        filho1.extend(crom2[ponto_cruzamento+1:self.tam_cromossomo+1])

        filho2.extend(crom2[0:ponto_cruzamento+1])
        filho2.extend(crom1[ponto_cruzamento+1:self.tam_cromossomo+1])

        print("Filhos: {} e {}".format(filho1, filho2))

        ret = []
        ret.append(filho1)
        ret.append(filho2)

        return ret
        
    def mutar(self):
        pass

    def roleta(self): # Seleção de pais para cruzamento
        qtd_individuos = self.tam_pop * self.taxa_cruzamento

        somatorio_pontuacoes = 0 # Total de pontos de todos os indivíduos para definir os que mais contribuem (esses são os melhores - cruzam)

        for key, value in self.populacao.items():
            somatorio_pontuacoes += value

        

    def avaliar_cromossomo(self, cromossomo):
        return self.func_avaliacao(cromossomo)

    def mostrar_pop(self):
        for elem in self.populacao: # falta mostrar o valor (tá mostrando somente as chaves, que são as tuplas)
            print(elem)

def avaliacao(cromossomo):
    aptidao = 0
    for elem in cromossomo:
        aptidao += elem

    return aptidao
ag01 = AG_real_coded(taxa_cruzamento, taxa_mutacao, 10, 5, 0, 6, avaliacao)

ag01.gerar_populacao_inicial()
ag01.mostrar_pop()

lista_chaves = list(ag01.populacao.keys())

ag01.cruzar(lista_chaves[0], lista_chaves[1], 2) # As chaves já são os genes do cromossomo
