import numpy as np
import matplotlib.pyplot as plt

predictions = np.genfromtxt('Redes/Predictions_SLP_D')
saidas = np.genfromtxt('PadraoD/SaidaD.txt')

print 'plotando...'
plt.plot(saidas, predictions, 'ro')
plt.show()
