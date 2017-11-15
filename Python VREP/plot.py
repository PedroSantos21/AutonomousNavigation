import numpy as np
import matplotlib.pyplot as plt

predictions = np.genfromtxt('Redes/Predictions_SLP_F')
saidas = np.genfromtxt('PadraoF/SaidaF.txt')

print 'plotando...'
plt.plot(saidas, predictions, 'ro')
plt.show()
