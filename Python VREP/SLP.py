import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD
import keras.backend as K

# Generate dummy data
import numpy as np
# x_train = np.random.random((1000, 20))
# y_train = keras.utils.to_categorical(np.random.randint(10, size=(1000, 1)), num_classes=10)
# x_test = np.random.random((100, 20))
# y_test = keras.utils.to_categorical(np.random.randint(10, size=(100, 1)), num_classes=10)


input_treinamento = np.genfromtxt('PadraoA/EntradaA.txt', delimiter=',')
output_treinamento= np.genfromtxt('PadraoA/SaidaA.txt', delimiter=',')

#input_teste = np.genfromtxt('testingsetx', delimiter=',')
#y_test = np.genfromtxt('testingsety', delimiter=';')

model = Sequential()

model.add(Dense(1, activation='tanh', input_dim=9, use_bias=True, bias_initializer='zeros'))
# model.add(Dropout(0.15))

sgd = SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='mean_squared_error',
             optimizer=sgd,
             metrics=['accuracy'])

model.fit(input_treinamento, output_treinamento, epochs=120, batch_size=1, verbose=1)

#score = model.evaluate(x_test, y_test, batch_size=1)

model.save('Redes/SLP_A.h5')

#prediction = model.predict(x_test, batch_size=1)
# print(prediction)
# print(y_test)
#np.savetxt('predictions.txt', prediction)
#test_y = np.reshape(y_test, (10000,1))
#print(np.concatenate((test_y, prediction), axis=1))
