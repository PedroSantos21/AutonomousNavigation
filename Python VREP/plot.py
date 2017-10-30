import numpy as np
import matplotlib.pyplot as plt

predictions = np.genfromtxt('Redes/Predictions_SLP_A_9')
saidas = np.genfromtxt('PadraoA/SaidaA.txt')

print 'plotando...'
plt.plot(saidas, predictions, 'ro')
plt.show()
