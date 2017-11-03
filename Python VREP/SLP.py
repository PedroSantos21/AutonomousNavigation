import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD
import keras.backend as K
import numpy as np


input_treinamento = np.genfromtxt('PadraoA/EntradaA.txt', delimiter=',')
output_treinamento= np.genfromtxt('PadraoA/SaidaA.txt', delimiter='None')
learning_rate = 0


learning_rate = 0.005
print "LR: ", learning_rate
model = Sequential()
model.add(Dense(units=1, activation='tanh', input_dim=9, use_bias=True, bias_initializer='zeros'))
sgd = SGD(lr=learning_rate, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='mean_squared_error',
         optimizer= sgd,
         metrics=['accuracy'])

model.fit(input_treinamento, output_treinamento, epochs=200, batch_size=1, verbose=1)
model.save('Redes/SLP_A_9.h5')
