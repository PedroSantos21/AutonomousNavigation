import numpy as np
import matplotlib.pyplot as plt

predictions = np.genfromtxt('Redes/Predictions_MLP_A_1')
saidas = np.genfromtxt('PadraoA/SaidaA.txt')

print 'plotando...'
plt.plot(saidas, predictions)
plt.show()
