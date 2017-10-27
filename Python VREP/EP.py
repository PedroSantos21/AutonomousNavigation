import random
from scipy.stats import norm
import numpy
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
        self.alpha = 1
        self.beta = 1
        self.fitness = 0.0

        self.Col = 0
        self.Osc = 0
        self.Lng = 0
        self.Arr = 0
        self.Clr = 0 #valores devem vir após teste da solução na simulação
        self.pesos = pesosIniciais
        self.cromossomo_size = 18

        for j in range(self.cromossomo_size):
            if(j < self.cromossomo_size/2):
                self.cromossomo.append(1)
            else:
                for peso in pesos:
                    self.cromossomo.append(peso)


    def setFitness(self, fitness):
        self.fitness = fitness;

    def getFitness(self):
        return self.fitness

    def setParam(self, Col, Osc, Lng, Arr, Clr):
        self.Col = Col
        self.Osc = Osc
        self.Lng = Lng
        self.Arr = Arr
        self.Clr = Clr


class EP:
    def __init__(self, pesosIniciais):
        self.population = []
        self.population_size = 30
        self.generations = 200
        self.elite_size = 3
        self.mutation_rate = 0.05
        self.tournament_size = 15

        #Self-adaptive mutation #Alterar valores de acordo com nosso problema
        self.St = 0.15  #Similarity Threshold
        self.Ma_min = 1
        self.Ma_max = 99 #Adaptive mutantion bounds
        self.delta_Ma = 1    #Adaptive Mutation incremet
        self.P_adaptive

        iniciaPopulacao(self.population_size, pesosIniciais)

        for cromossomo in self.population:
            evaluation(cromossomo)
            #aqui a condição de parada também precisa ser alterada --> ok
        for generation in range(generations):
            print "Generation: "+str(generation)
            #condição de parada
            for i in range(population_size):
                if self.fitness[i] <= 80.0:
                    print "Condição de Parada: Fitness"
                    break

            for cromossomo in self.population:
                #mutation
                mutation(self.population)
                #evaluation então, aqui que tem que fazer a integração com a rede
                cromossomo.setParam(Col, Osc, Lng, Arr, Clr)
                evaluation(cromossomo)

            #selection
            selection(self.population)


    def iniciaPopulacao(self, population_size, pesos):
        for i  in range(population_size):
            self.population.append(cromossomo(pesos))


    def evaluation(self, cromossomo): #nova forma?? daqui pra baixo tá minha dúvida, como acha que seria melhor, po
        self.verificaCusto_S(cromossomo)
        self.verificaCusto_P(cromossomo)
        cromossomo.setFitness((self.alfa*self.custoS) + (self.beta*self.custoP))  #certo? então,aí que está esses parametros teriam que já ser atualizados diretamente no cromossomo ok?

    def verificaCusto_P(cromossomo):
        cromossomo.custoP = 0
        cromossomo.custoP = cromossomo.custoP + (cromossomo.Q1*(cromossomo.Col*10000) + cromossomo.Q2*(cromossomo.Osc*0.1) + cromossomo.Q3*cromossomo.Lng + cromossomo.Q4*(cromossomo.Arr*100) + cromossomo.Q5*(1 - cromossomo.Clr))

    def verificaCusto_S(cromossomo):
        cromossomo.custoS = 0
        for i in range(cromossomo.cromossomo_size):
            if(i < 9):
                cromossomo.custoS  = cromossomo.custoS + cromossomo[i]

    def selection(self):
        elite = []
        #Rank-based --
        rank_based = sorted(self.fitness)
        for i in rang(rank_based):
            if (i < 3):
                elite = rank_based[i]
            else:

    #Self-adaptive mutation
    def mutation(self):
        similar = similarity(self.population)
        if(similar >= self.St):
            self.P_adaptive = self.P_adaptive + self.delta_Ma
        else:
            self.P_adaptive = self.P_adaptive - self.delta_Ma

    #define o nivel de similaridade da populacao
    def similarity(self):
        similar = 0
        matched = False
        length = self.population_size

        rank = sorted(self.fitness)

        for i in range(length-1):

            if (rank[i] == rank[i+1]):
                similar = similar + 1
                matched = True
            elif (matched):
                similar = similar + 1
                matched = False

            #se esta na ultima posicao
            if(matched &  (i+1 == length - 1)):
                similar = similar + 1
        return (similar/length)
