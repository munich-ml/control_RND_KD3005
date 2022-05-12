# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 11:07:49 2019

@author: holge
"""

import numpy as np
from time import sleep
import matplotlib.pyplot as plt
from kd3005p import kd3005pInstrument

VSTART = 0
VSTOP = 3
VSTEP = 0.05
AMAX = 0.1
TSLEEP =0.1
voltages = np.arange(VSTART, VSTOP+VSTEP, VSTEP)
currents = list()

psu = kd3005pInstrument('COM6')
if psu.isConnected:
    print(psu.getIdn())
    psu.setAmp(AMAX)
    for v in voltages:
        psu.setVolt(v)
        sleep(TSLEEP)
        cur = float(psu.readAmp())*1000
        currents.append(cur)
        print(str(v) + "V, " + str(cur) + "mA, stat=" + str(psu.status))
    psu.setVolt(0)
psu.close()	


fig = plt.figure(figsize=(7, 5))
ax = fig.add_subplot(111)
ax.plot(voltages, currents, "o:")
ax.grid(True)
ax.set(title="IV curve", xlabel='voltage [V]', ylabel="current [mA]")
#plt.savefig("IV.png")
#sleep(0.1)    
plt.show()
        