import math
class modulo():
    def __init__ (self, padroes):
        self.padroes = padroes

    def getPadrao(self):
        return self.padroes

class blending():
    def __init__ (self):
        self.leituras = []
        self.distancias = []
        self.pesos = []
        self.modulo = []

        self.NUM_MODULOS = 9
        self.NUM_SENSORES = 8

        #inicializa os padroes de leitura
        self.padroes1 = [1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000]
        self.padroes2 = [0.1490, 0.1923, 0.3017, 0.7409, 0.7360, 0.2475, 0.1574, 0.1216]
        self.padroes3 = [0.0401, 0.0540, 0.0957, 0.2928, 0.5619, 0.0979, 0.0556, 0.0405]
        self.padroes4 = [0.0533, 0.0709, 0.1211, 0.3608, 0.5584, 0.6299, 0.4920, 0.3873]
        self.padroes5 = [0.5578, 0.7116, 0.6337, 0.5647, 0.2460, 0.0820, 0.0454, 0.0327]
        self.padroes6 = [0.0534, 0.2330, 0.3011, 0.3213, 0.3228, 0.3609, 0.2754, 0.2172]
        self.padroes7 = [0.2244, 0.2917, 0.3518, 0.3134, 0.3154, 0.2722, 0.3010, 0.0573]
        self.padroes8 = [1.0000, 1.0000, 0.9194, 0.1323, 0.1324, 0.8444, 1.0000, 1.0000]
        self.padroes9 = [0.0401, 0.0523, 0.3796, 0.0983, 0.0984, 0.3799, 0.0539, 0.0406]

        #inicializando vetor de modulo de acordo com os padroes
        self.modulo.append(modulo(self.padroes1))
        self.modulo.append(modulo(self.padroes2))
        self.modulo.append(modulo(self.padroes3))
        self.modulo.append(modulo(self.padroes4))
        self.modulo.append(modulo(self.padroes5))
        self.modulo.append(modulo(self.padroes6))
        self.modulo.append(modulo(self.padroes7))
        self.modulo.append(modulo(self.padroes8))
        self.modulo.append(modulo(self.padroes9))

        #inicializando vetores da classe
        for i in range(self.NUM_MODULOS):
            self.distancias.append(-1)
            self.pesos.append(-1)

        self.davg = 0
        for  i in range(self.NUM_MODULOS):
            for j in range(self.NUM_MODULOS):
                self.davg = self.davg + self.distanciaEuclidiana(self.modulo[i].getPadrao(), self.modulo[j].getPadrao())

        self.davg = self.davg/(self.NUM_MODULOS**2)
        self.threshold = self.davg/2.0

    #Calcula a distancia euclidiana entre dois vetores
    def distanciaEuclidiana(self, vetor1, vetor2):
        soma = 0
        for i in range(len(vetor1)):
            soma = soma + (vetor1[i]-vetor2[i])**2
        return math.sqrt(soma)

    #Encontra o padrao a partir das leituras atuais
    def definePadrao(self):
        padrao = 0
        menorDist = 1000000

        for i in range(self.NUM_MODULOS):
            self.distancias[i] = self.distanciaEuclidiana(self.modulo[i].getPadrao(), self.leituras)

        for i in range(self.NUM_MODULOS):
                if(self.distancias[i] < menorDist):
                    padrao = i+1
                    menorDist = self.distancias[i]

        #se a menor distancia for maior que o threshold aplica blending (envia padrao -1)
        if(menorDist > self.threshold):
            padrao = -1

        return padrao

    #Calcula os pesos do blending
    def calculaPesos(self, padrao):
        soma = 0
        if(padrao == -1):
            for i in range(self.NUM_MODULOS):
                soma = soma + (self.davg - self.distancias[i])**2

            for i in range(self.NUM_MODULOS):
                self.pesos[i] = ((self.davg-self.distancias[i])**2)/soma
        else:
            for i in range(self.NUM_MODULOS):
                self.pesos[i] = 0
            self.pesos[padrao-1] = 1
        return self.pesos


    def getThreshold(self):
        return self.threshold

    #seta as leituras atuais (NORMALIZADAS)
    def setLeituras(self, leituras):
        self.leituras = leituras
