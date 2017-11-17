# -*- coding: utf-8 -*-
import random
from scipy.stats import norm
import numpy
import EP2SLP
#PARÂMETROS DO EP --> EP diferencia-se de AG pelo uso somente de mutação
class cromossomo():
    def __init__ (self, pesosIniciais):
        #Funçao de Custo
        self.custoTotal = 0
        self.custoS = 0
        self.custoP = 0
        self.Q1 = 1
        self.Q2 = 1
        self.Q3 = 1
        self.Q4 = 1
        self.Q5 = 1
        self.alfa = 1
        self.beta = 1
        self.fitness = 0

        self.Col = 0
        self.Osc = 0
        self.Lng = 0
        self.Arr = 0
        self.Clr = 0 #valores devem vir após teste da solução na simulação
        self.pesos = list(pesosIniciais)
        self.cromossomo_size = 18
        self.genes = []

        for j in range(self.cromossomo_size):
            if(j < self.cromossomo_size/2):
                self.genes.append(1)
        for peso in pesos:
            self.genes.append(peso)

    def setGenes(self, posicao, valor):
        self.genes[posicao] = valor

    def getGenes(self):
        return self.genes

    def setFitness(self, fitness):
        self.fitness = fitness

    def getFitness(self):
        return self.fitness

    def setParam(self, Col, Osc, Lng, Arr, Clr):
        self.Col = Col
        self.Osc = Osc
        self.Lng = Lng
        self.Arr = Arr
        self.Clr = Clr


class EP:
    def __init__(self, pesosIniciais, ambiente, posicaoInicial):
        self.population = []
        self.population_size = 5
        self.generations = 200
        self.elite_size = 3
        self.mutation_rate = 2   #Quantidade de genes a serem mutados
        self.tournament_size = 15

        #Self-adaptive mutation #Alterar valores de acordo com nosso problema
        self.St = 0.15  #Similarity Threshold
        self.Ma_min = 1
        self.Ma_max = 99 #Adaptive mutantion bounds
        self.delta_Ma = 10    #Adaptive Mutation incremet
        self.P_adaptive = 0
        self.next_generation = []
        self.best_fitness = 100000
        self.fitness_list = []
        self.intensidadeMutacao = 0.1
        convergiu = False

        self.iniciaPopulacao(self.population_size, pesosIniciais)

        for cromossomo in self.population:
            Col, Osc, Lng, Arr, Clr = EP2SLP.getParametros(ambiente, posicaoInicial, cromossomo.getGenes())
            print "Col: ", Col, ", Osc: ", Osc, ", Lng: ",Lng,", Arr: ", Arr,", Clr: ",Clr
            cromossomo.setParam(Col, Osc, Lng, Arr, Clr)
            self.evaluation(cromossomo)
            print "Fitness: ", cromossomo.getFitness()
        self.sort_fitness()

        for generation in range(self.generations):
            self.next_generation = []
            print "Generation: "+str(generation)

            #CHECA SE JA TERMINOU
            for cromossomo in self.population:
                if self.best_fitness <= 30.0:
                    print "CONVERGIU COM ", self.best_fitness
                    convergiu = True
                    for cromossomo in self.population:
                        if self.best_fitness == cromossomo.fitness:
                            EP2SLP.salvarRede(cromossomo.getGenes())
                            break
                    break
            if convergiu:
                print "-----------FIM------------"
                break

            for cromossomo in self.population:
                self.mutation(cromossomo)    #mutation
                Col, Osc, Lng, Arr, Clr = EP2SLP.getParametros(ambiente, posicaoInicial,cromossomo.getGenes())
                print "Col: ", Col, ", Osc: ", Osc, ", Lng: ",Lng,", Arr: ", Arr,", Clr: ",Clr
                cromossomo.setParam(Col, Osc, Lng, Arr, Clr)
                self.evaluation(cromossomo)            #evaluation então, aqui que tem que fazer a integração com a rede
                print "Fitness: ", cromossomo.getFitness()
            self.sort_fitness()

            print "------------SELECAO------------"
            self.selection()

            for cromossomo in self.population:      #restante dos elementos são mutados para serem levados a proxima geração
                self.mutation(cromossomo)
                self.next_generation.append(cromossomo)

            print "---------NEXT GENERATION---------"
            #print self.next_generation
            for cromossomo in self.next_generation:
                print cromossomo.getGenes()
            self.population = list(self.next_generation)

    def iniciaPopulacao(self, population_size, pesos):
        for i  in range(population_size):
            self.population.append(cromossomo(pesos))
        print "----------POPULACAO INICIAL-------------"

        for individuo in self.population:
            print individuo.getGenes()

    def evaluation(self, cromossomo):
        self.verificaCusto_S(cromossomo)
        self.verificaCusto_P(cromossomo)
        cromossomo.setFitness((cromossomo.alfa*cromossomo.custoS) + (cromossomo.beta*cromossomo.custoP))

    def verificaCusto_P(self, cromossomo):
        cromossomo.custoP = 0
        if cromossomo.Col:
            cromossomo.custoP = cromossomo.custoP + cromossomo.Q1*10000

        if not cromossomo.Arr:
            cromossomo.custoP = cromossomo.custoP + cromossomo.Q4*100

        cromossomo.custoP =  cromossomo.custoP + cromossomo.Q2*(cromossomo.Osc*0.1) + cromossomo.Q3*cromossomo.Lng + cromossomo.Q5*cromossomo.Clr

    def verificaCusto_S(self, cromossomo):
        for i in range(cromossomo.cromossomo_size):
            if(i < 9):
                cromossomo.custoS  = cromossomo.custoS + cromossomo.getGenes()[i]

    def selection(self):
        print "---------ELITISMO---------"
        self.elitism()
        print "---------TORNEIO---------"
        for i in range(self.tournament_size):
            self.tournament_selection()

    def sort_fitness(self):
        self.fitness_list = []
        for cromossomo in self.population:
            self.fitness_list.append(cromossomo.fitness)
        self.fitness_list = sorted(self.fitness_list)
        print "MELHOR FITNESS: ", self.fitness_list[0]
        self.best_fitness = self.fitness_list[0]

    def elitism(self):
        #Rank-based
        for i in range(3):
            for cromossomo in self.population:
                if self.fitness_list[i] == cromossomo.fitness:
                    self.next_generation.append(cromossomo)
                    self.population.remove(cromossomo)
                    break

    def tournament_selection(self):
        #implements tournament selection
        #select fighters randomly popSize-1 times (elitism takes one slot)
        if len(self.population) > 1:
            p1index = random.randint(0, len(self.population)-1)
            p2index = random.randint(0, len(self.population)-1)

            print "P1: ", p1index, " P2: ", p2index, " len: ", len(self.population)
            while(p2index == p1index):
                p2index = random.randint(0, len(self.population)-1)
                print "P1: ", p1index, " P2: ", p2index, " len: ",       len(self.population)

            cromossomo1 = self.population[p1index]
            cromossomo2 = self.population[p2index]

            winner = self.fight(cromossomo1, cromossomo2)
            #print 'adding %sth parent'%str(i)
            self.next_generation.append(winner)
            self.population.remove(winner)

    def fight(self, cromossomo1, cromossomo2):
        #fights the chromosome passed in as parameter (opponent)
        fitness1 = cromossomo1.fitness
        fitness2 = cromossomo2.fitness

        if fitness1 < fitness2:
            return cromossomo1
        else:
            return cromossomo2

    #Self-adaptive mutation
    def mutation(self, cromossomo):
        print "-------MUTACAO--------"
        genesMutados = []
        similar = self.similarity()
        print "Similar ", similar
        if(similar >= self.St):
            self.P_adaptive = self.P_adaptive + self.delta_Ma
        else:
            if self.P_adaptive > 0:
                self.P_adaptive = self.P_adaptive - self.delta_Ma

        print "P_adaptive: ", self.P_adaptive

        probability = random.randint(0, 100)

        if(probability <= self.P_adaptive):
            print "------MUTOU-------"
            for i in range(self.mutation_rate):
                gene = random.randint(cromossomo.cromossomo_size/2, cromossomo.cromossomo_size-1)

                while(gene in genesMutados):
                   gene = random.randint(cromossomo.cromossomo_size/2, cromossomo.cromossomo_size-1)
                print "Gene mutado: ", gene
                incremento = (cromossomo.getGenes()[gene])*self.intensidadeMutacao
                fatorAditivo = random.randint(1, 3)  #fator para definir se será decremento ou incremento
                if(fatorAditivo == 1):   #soma
                    cromossomo.setGenes(gene, (incremento+cromossomo.getGenes()[gene]))
                else:
                    cromossomo.setGenes(gene, (-incremento+cromossomo.getGenes()[gene]))

                genesMutados.append(gene)

    #define o nivel de similaridade da populacao
    def similarity(self):
        fitness_list = []
        similar = 0.0
        matched = False
        length = len(self.population)

        self.sort_fitness()
        rank = []
        for fitness in self.fitness_list:
            rank.append(round(fitness))

        for i in range(length-1):
            if (rank[i] >= rank[i+1] - 2 and rank[i] <= rank[i+1]+2):
                similar = similar + 1.0
                matched = True
                print "MATCH"
            elif (matched):
                similar = similar + 1.0
                matched = False

            #se esta na ultima posicao
            if(matched and (i+1 == length-1)):
                similar = similar + 1.0
        return (similar/length)*1.0

EP2SLP.init()

ambiente = raw_input('Qual Padrao de ambiente o robo sera inserido? ')
posicaoInicial = raw_input('Qual a posicao inicial do robo? ')

pesosIniciais = EP2SLP.getPesosIniciais(ambiente)
#print pesosIniciais
pesos = []
for valor in pesosIniciais[0]:
    pesos.append(valor[0])
#print pesos
ep = EP(pesos, ambiente, posicaoInicial)
