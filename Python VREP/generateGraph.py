#coding: utf-8
import matplotlib.pyplot as plt
import numpy as np

plt.rcdefaults()
#fig, ax = plt.subplots()
padroes1 = [1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000]
padroes2 = [0.1490, 0.1923, 0.3017, 0.7409, 0.7360, 0.2475, 0.1574, 0.1216]
padroes3 = [0.0401, 0.0540, 0.0957, 0.2928, 0.5619, 0.0979, 0.0556, 0.0405]
padroes4 = [0.0533, 0.0709, 0.1211, 0.3608, 0.5584, 0.6299, 0.4920, 0.3873]
padroes5 = [0.5578, 0.7116, 0.6337, 0.5647, 0.2460, 0.0820, 0.0454, 0.0327]
padroes6 = [0.0534, 0.2330, 0.3011, 0.3213, 0.3228, 0.3609, 0.2754, 0.2172]
padroes7 = [0.2244, 0.2917, 0.3518, 0.3134, 0.3154, 0.2722, 0.3010, 0.0573]
padroes8 = [1.0000, 1.0000, 0.9194, 0.1323, 0.1324, 0.8444, 1.0000, 1.0000]
padroes9 = [0.0401, 0.0523, 0.3796, 0.0983, 0.0984, 0.3799, 0.0539, 0.0406]

x_axis = [1,2,3,4,5,6,7,8]

f, axarr = plt.subplots(3, 3)

axarr[0, 0].bar(x_axis, padroes1, tick_label=x_axis)
axarr[0, 0].set_title('Padrao A')

axarr[0, 1].bar(x_axis, padroes2, tick_label=x_axis)
axarr[0, 1].set_title('Padrao B')

axarr[0, 2].bar(x_axis, padroes3, tick_label=x_axis)
axarr[0, 2].set_title('Padrao C')

axarr[1, 0].bar(x_axis, padroes4, tick_label=x_axis)
axarr[1, 0].set_title('Padrao D')

axarr[1, 1].bar(x_axis, padroes5, tick_label=x_axis)
axarr[1, 1].set_title('Padrao E')

axarr[1, 2].bar(x_axis, padroes6, tick_label=x_axis)
axarr[1, 2].set_title('Padrao F')

axarr[2, 0].bar(x_axis, padroes7, tick_label=x_axis)
axarr[2, 0].set_title('Padrao G')

axarr[2, 1].bar(x_axis, padroes8, tick_label=x_axis)
axarr[2, 1].set_title('Padrao H')

axarr[2, 2].bar(x_axis, padroes9, tick_label=x_axis)
axarr[2, 2].set_title('Padrao I')

f.subplots_adjust(hspace=0.4)



plt.show()
