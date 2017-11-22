import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD
import keras.backend as K
import numpy as np


input_txt = np.genfromtxt('PadraoG/EntradaG.txt', delimiter=',')
output_treinamento= np.genfromtxt('PadraoG/SaidaG.txt', delimiter='None')

input_treinamento = []
for vetor in input_txt:
	input_treinamento.append([vetor[5], vetor[6]])
	

input_treinamento = np.array(input_treinamento)

#print input_treinamento

model = Sequential()

model.add(Dense(units=1, activation='tanh', input_dim=2, use_bias=False))
sgd = SGD(lr=0.0005, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='mean_squared_error',
             optimizer= sgd,
             metrics=['accuracy'])

model.fit(input_treinamento, output_treinamento, epochs=200, batch_size=1, verbose=0)

model.save('Redes/SLP_G.h5')
