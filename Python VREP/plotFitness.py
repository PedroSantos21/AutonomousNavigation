#coding: utf-8
from __future__ import unicode_literals
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter, MaxNLocator


fig = plt.figure()
ax = fig.add_subplot(111)

inputs = np.genfromtxt('best_fitnessI.txt', delimiter='None')
x_axis = []
limiar = []

for i in range(len(inputs)):
	x_axis.append(i)
	limiar.append(50)

ax.xaxis.set_major_locator(MaxNLocator(integer=True))
line1, = ax.plot(x_axis, inputs)	
line2, = ax.plot(x_axis, limiar, 'r--')	
plt.xlabel('Geração')
plt.legend([line1, line2], ['Fitness', 'Limiar'])
plt.show()
