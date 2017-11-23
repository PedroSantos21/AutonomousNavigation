#coding: utf-8
import keras
import math
import numpy as np
import keras.backend as K
from keras.models import Model
from keras.models import load_model
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD
from pynput import keyboard

model =  load_model('Redes/SLP_G.h5')
slp_model = Model(inputs=model.input, outputs=model.output)

pesos = [0.04882535, -0.07291704, 0.02149473, 0.00387635, 0.00589686, -0.01891204, -0.01967716, -0.01013027, -0.03803024]

pesos_rede = []
for i in range(len(pesos)):
    pesos_rede.append([pesos[i]])
slp_model.get_layer(name=None, index=1).set_weights([np.array(pesos_rede)])

sgd = SGD(lr=0.0005, decay=1e-6, momentum=0.9, nesterov=True)
slp_model.compile(loss='mean_squared_error', optimizer= sgd, metrics=['accuracy'])

slp_model.save('Redes/SLP_G_2.h5')
