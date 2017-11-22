from keras.models import load_model
import numpy as np


model = load_model('Redes/SLP_A_12.h5')
inputs = np.genfromtxt('PadraoA/EntradaA.txt', delimiter=',')
predictions = []

for entrada in inputs:
    pred = model.predict(np.array([entrada]), batch_size=1, verbose=0)
    predictions.append(pred)

np.savetxt(fname='Redes/Predictions_SLP_A_12', X=predictions)
print "Predicoes Geradas!"
