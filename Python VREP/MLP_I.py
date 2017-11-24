import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD
import keras.backend as K
import numpy as np


input_treinamento = np.genfromtxt('PadraoI/EntradaI.txt', delimiter=',')
output_treinamento= np.genfromtxt('PadraoI/SaidaI.txt', delimiter='None')

"""
input_treinamento = []

for vetor in input_txt:
	input_treinamento.append([vetor[2], vetor[5], vetor[7], vetor[8]])
"""
model = Sequential()

#model.add(Dense(units=1, activation='tanh', input_dim=4, use_bias=False))

model.add(Dense(9, activation='tanh', input_dim=9, use_bias=True, bias_initializer='zeros'))
#"Hidden" Layer
model.add(Dense(3, activation='tanh', use_bias=True, bias_initializer='zeros'))
#Output Layer
model.add(Dense(1, activation='tanh', use_bias=True, bias_initializer='zeros'))


sgd = SGD(lr=0.0005, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='mean_squared_error',
             optimizer= sgd,
             metrics=['accuracy'])

model.fit(input_treinamento, output_treinamento, epochs=500, batch_size=1, verbose=1)

model.save('Redes/MLP_I.h5')
