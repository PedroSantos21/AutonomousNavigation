import random
from scipy.stats import norm
import numpy
#PARÂMETROS DO EP --> EP diferencia-se de AG pelo uso somente de mutação

input_target = None
input_target_length = None

class EP:
    def __init__(self, pesosIniciais):
        self.cromossomo = []
        self.population = []
        self.population_size = 30
        self.cromossomo_size = 18
        self.generations = 200
        self.elite_size = 3
        self.mutation_rate = 0.05
        self.tournament_size = 15
        self.fitness = []

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

        iniciaPopulacao(self.population_size, pesosIniciais)
        #envia pesos pra rede e recebe os valores para calcular o fitness de todos os
        # Col, Osc, Lng, Arr, Clr =
        calculaFitness(self.population, Col, Osc, Lng, Arr, Clr)

        for generation in range(generations):
            print "Generation: "+str(generation)
            #condição de parada
            for i in range(population_size):
                if self.fitness[i] <= 80.0:
                    print "Condição de Parada: Fitness"
                    break
            #mutation
            #evaluation
            #selection
            populacao = mutation(populacao)
            #envia pesos pra rede e recebe os valores para calcular o fitness de todos os
            # Col, Osc, Lng, Arr, Clr =
            calculaFitness(self.population, Col, Osc, Lng, Arr, Clr)
            populacao = selection(populacao)



    def iniciaPopulacao(self, population_size, pesos):
        for i  in range(population_size):
            for j in range(self.cromossomo_size):
                if(j < self.cromossomo_size/2):
                    self.cromossomo.append(1)
                else:
                    for peso in pesos:
                        self.cromossomo.append(peso)
            self.population.append(self.cromossomo)
            self.cromossomo = []

    def calculaFitness(self, Col, Osc, Lng, Arr, Clr):
        for cromossomo in self.population:
            self.verificaCusto_S(cromossomo)
            self.verificaCusto_P(Col, Osc, Lng, Arr, Clr)
            self.fitness.append((self.alfa*self.custoS) + (self.beta*self.custoP))

    def verificaCusto_P(Col, Osc, Lng, Arr, Clr):
        self.custoP = 0
        self.custoP = self.custoP + (self.Q1*(Col*10000) + self.Q2*(Osc*0.1) + self.Q3*Lng + self.Q4*(Arr*100) + self.Q5*(1 - Clr))

    def verificaCusto_S(cromossomo):
        self.custoS = 0
        for i in range(cromossomo):
            if(i < 9):
                self.custoS = self.custoS + cromossomo[i]

    def selection(self):
        elite = []
        #Rank-based
        rank_based = sorted(self.fitness)
        for i in rang(rank_based):
            if (i < 3):
                elite = rank_based[i]
            else:


    def mutation(self):
        for
