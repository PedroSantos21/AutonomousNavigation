import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD
import keras.backend as K
import numpy as np


input_treinamento = np.genfromtxt('PadraoB/EntradaB.txt', delimiter=',')
output_treinamento= np.genfromtxt('PadraoB/SaidaB.txt', delimiter='None')

model = Sequential()

model.add(Dense(units=1, activation='tanh', input_dim=9, use_bias=True, bias_initializer='zeros'))
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='mean_squared_error',
             optimizer= sgd,
             metrics=['accuracy'])

model.fit(input_treinamento, output_treinamento, epochs=100, batch_size=1, verbose=1)

model.save('Redes/SLP_B_1.h5')
