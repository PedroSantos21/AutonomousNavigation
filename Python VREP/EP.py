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
        self.next_generation = []
        iniciaPopulacao(self.population_size, pesosIniciais)

        for cromossomo in self.population:
            evaluation(cromossomo)
            #aqui a condição de parada também precisa ser alterada --> ok
        for generation in range(generations):
            print "Generation: "+str(generation)
            #condição de parada
            #ARRUMAR LEITAO
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


    def evaluation(self, cromossomo):
        self.verificaCusto_S(cromossomo)
        self.verificaCusto_P(cromossomo)
        cromossomo.setFitness((cromossomo.alfa*cromossomo.custoS) + (cromossomo.beta*cromossomo.custoP))

    def verificaCusto_P(self, cromossomo):
        #cromossomo.custoP = 0
        cromossomo.custoP = (cromossomo.Q1*(cromossomo.Col*10000) + cromossomo.Q2*(cromossomo.Osc*0.1) + cromossomo.Q3*cromossomo.Lng + cromossomo.Q4*(cromossomo.Arr*100) + cromossomo.Q5*cromossomo.Clr)

    def verificaCusto_S(self, cromossomo):
        for i in range(cromossomo.cromossomo_size):
            if(i < 9):
                cromossomo.custoS  = cromossomo[i]

    def selection(self):
        elitism()
        for i in range(tournament_size):
            self.tournament_selection()

    def elitism(self):
        #Rank-based
        for cromossomo in self.population:
            fitness_list.append(cromossomo.fitness)
        rank_based = sorted(fitness_list)
        for i in range(3):
            for cromossomo in self.population:
                if rank_based[i] == cromossomo.fitness:
                    next_generation.append(cromossomo)
                    self.population.remove(cromossomo)
                    break

    def tournament_selection(self):
        #implements tournament selection
        #randomly select 2 and have them fight to get into parentPool

        for i in range(self.population_size):
            #select fighters randomly popSize-1 times (elitism takes one slot)
            p1index = random.randint(0,self.population_size)
            p2index = random.randint(0,self.population_size)
            while(p2index == p1index):
                p2index = random.randint(0, self.population_size)

            cromossomo1 = self.population[p1index]
            cromossomo2 = self.population[p2index]

            winner = fight(cromossomo1, cromossomo2)
            #print 'adding %sth parent'%str(i)
            self.next_generation.append(winner)

    def fight(self, cromossomo1, cromossomo2):
        #fights the chromosome passed in as parameter (opponent)
        fitness1 = cromossomo1.fitness
        fitness2 = cromossomo2.fitness

        if fitness1 < fitness2:
            return cromossomo1
        else:
            return cromossomo2



    #Self-adaptive mutation
    def mutation(self):
        similar = self.similarity()
        if(similar >= self.St):
            self.P_adaptive = self.P_adaptive + self.delta_Ma
        else:
            self.P_adaptive = self.P_adaptive - self.delta_Ma

    #define o nivel de similaridade da populacao
    def similarity(self):
        fitness_list = []
        similar = 0
        matched = False
        length = self.population_size

        for cromossomo in self.population:
            fitness_list.append(cromossomo.fitness)

        rank = sorted(fitness_list)

        for i in range(length):
            if (rank[i] == rank[i+1]):
                similar = similar + 1
                matched = True
            elif (matched):
                similar = similar + 1
                matched = False

            #se esta na ultima posicao
            if(matched and (i+1 == length)):
                similar = similar + 1
        return (similar/length)
