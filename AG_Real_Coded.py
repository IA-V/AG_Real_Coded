import random
import math

taxa_cruzamento = .8
taxa_mutacao = .05
taxa_elitismo = .5

class AG_real_coded:
    populacao = dict()
    sobreviventes = []
    filhos = []
    
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
        #print("Pais: {} e {}".format(crom1, crom2))
        
        filho1 = []
        filho2 = []

        filho1.extend(crom1[0:ponto_cruzamento+1])
        filho1.extend(crom2[ponto_cruzamento+1:self.tam_cromossomo+1])

        filho2.extend(crom2[0:ponto_cruzamento+1])
        filho2.extend(crom1[ponto_cruzamento+1:self.tam_cromossomo+1])

        #print("Filhos: {} e {}".format(filho1, filho2))

        filho1 = tuple(filho1)
        filho2 = tuple(filho2)

        # Adiciona filhos a uma lista de individuos que fará parte da próxima geração
        self.filhos.append(filho1)
        self.filhos.append(filho2)

        # Adiciona os filhos à população
        self.populacao[filho1] = self.avaliar_cromossomo(filho1)
        self.populacao[filho2] = self.avaliar_cromossomo(filho2)

        #ret = []
        #ret.append(filho1)
        #ret.append(filho2)

        #return ret
        
    def mutar(self):
        pass

    def ordenar_pop(self):
        self.populacao = dict(sorted(self.populacao.items(), key=lambda item: item[1])) # Ordem crescente de pontuações

    def roleta(self): # Seleção de pais para cruzamento
        qtd_individuos = self.tam_pop * self.taxa_cruzamento # Qtd de novos indivíduos
        qtd_pais = math.floor(qtd_individuos / 2)  # Qtd de pais para os indivíduos da nova geração (apenas metade da qtd de novos indivíduos, já que o cruzamento gera dois novos indivíduos)
        pais = [] # Lista de chaves dos indivíduos selecionados para cruzamento

        somatorio_pontuacoes = 0 # Total de pontos de todos os indivíduos para definir os que mais contribuem (esses são os melhores - cruzam)

        for key, value in self.populacao.items():
            somatorio_pontuacoes += value

        self.ordenar_pop()
        # self.populacao = dict(sorted(self.populacao.items(), key=lambda item: item[1])) # Ordem crescente de pontuações

        idx_individuo = self.tam_pop - 1
        
        while(len(pais) < qtd_pais): # Itera sobre os indivíduos até adicionar a qtd necessária de pais
            percentagem = random.uniform(0, 1)

            pontuacao_individuo_atual = list(self.populacao.values())[idx_individuo]
            chave_individuo_atual = list(self.populacao)[idx_individuo]

            aptidao_individuo_atual = pontuacao_individuo_atual / somatorio_pontuacoes

            if((1-percentagem) <= aptidao_individuo_atual and chave_individuo_atual not in pais): # Condição para selecionar indivíduo atual na roleta
                pais.append( list(self.populacao)[idx_individuo] )

            if(idx_individuo == -1):
                idx_individuo = self.tam_pop - 1

            idx_individuo -= 1

        print("Os pais são:\n{}\n".format(pais))

        return pais

    def elitismo(self): # Seleciona apenas os melhores indivíduos da geração atual para sobreviverem
        self.ordenar_pop()
        lista_pop = list(self.populacao) # Lista de chaves (cromossomos)
        qtd_sobreviventes = math.floor(len(lista_pop) * taxa_elitismo)
        
        idx = len(lista_pop)-1

        #print(lista_pop)

        while(idx >= 0 and len(self.sobreviventes) < qtd_sobreviventes):
            if (lista_pop[idx] not in self.filhos):
                self.sobreviventes.append(lista_pop[idx])
            idx -= 1

    def proxima_geracao(self): # Remove indivíduos que não estão aptos para a próxima geração
        cromossomos = list(self.populacao)

        #print("Qtd sobreviventes:{}".format(len(self.sobreviventes)))
        #print("Qtd filhos novos:{}".format(len(self.filhos)))

        for key in cromossomos:
            if key not in self.sobreviventes and key not in self.filhos:
                del self.populacao[key]

        self.sobreviventes.clear()
        self.filhos.clear()

    def avaliar_cromossomo(self, cromossomo):
        return self.func_avaliacao(cromossomo)

    def mostrar_pop(self):
        for key, value in self.populacao.items():
            print("\n{}:{}\n".format(key, value))

        print("Tamanho da população atual: {}".format(len(self.populacao)))

def avaliacao(cromossomo):
    aptidao = 0
    for elem in cromossomo:
        aptidao += elem

    return aptidao

# Instanciamento de um objeto AG_real_coded
ag01 = AG_real_coded(taxa_cruzamento, taxa_mutacao, 10, 5, 0, 6, avaliacao)

ag01.gerar_populacao_inicial()
ag01.mostrar_pop()

lista_chaves = list(ag01.populacao.keys())

#ag01.cruzar(lista_chaves[0], lista_chaves[1], 2) # As chaves já são os genes do cromossomo

pais = ag01.roleta()
print("LEN PAIS: {}".format(len(pais)))

if (len(pais) % 2 == 0):
    for i in range(0, len(pais), 2):
        ag01.cruzar(lista_chaves[i], lista_chaves[i+1], 2)
else:
    for i in range(0, len(pais), 2):
        print(i, len(pais)-1)
        if(i == len(pais)-1):
            ag01.cruzar(lista_chaves[i], lista_chaves[i-2], 2)
        else:
            ag01.cruzar(lista_chaves[i], lista_chaves[i+1], 2)

print("Qtd de filhos novos: {}".format( len(ag01.filhos) ))
ag01.elitismo()
print("Qtd de sobreviventes: {}".format( len(ag01.sobreviventes) ))
ag01.proxima_geracao()
#ag01.cruzar(lista_chaves[i], lista_chaves[i-1])
    
ag01.mostrar_pop()
