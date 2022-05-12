# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 11:07:49 2019

@author: holge
"""

from time import sleep
import datetime as dt
import matplotlib.pyplot as plt
from kd3005p import kd3005pInstrument

AMAX = 1
VOLTAGE = 24
TSLEEP = 1

datetimes = list()
currents = list()
voltages = list()

psuNoneTypeCnt = 0
psu = kd3005pInstrument('COM6')

if psu.isConnected:
    print("Connected to " + psu.getIdn())
    psu.setAmp(AMAX)
    psu.setVolt(VOLTAGE)
    try:
        while True:
            now = dt.datetime.now()
            cur = psu.readAmp()
            vol = psu.readVolt()
            if cur is not None and vol is not None:                
                datetimes.append(now)
                currents.append(float(cur)*1000)
                voltages.append(float(vol))
                print(str(datetimes[-1]).split(".")[0] + ", " + 
                      str(currents[-1]) + "mA, " + 
                      str(voltages[-1]) + "V")
            else:
                psuNoneTypeCnt += 1
                print("NoneType read form PSU: " + str(psuNoneTypeCnt) + " times")
            sleep(TSLEEP)
    except KeyboardInterrupt:
        print("keyboard interrupt")

print("Disconnecting from PowerSupply")
psu.setVolt(0)
psu.close()	


# equalize length of lists
length = min(len(datetimes), len(currents), len(voltages))
currents = currents[:length]
voltages = voltages[:length]
datetimes = datetimes[:length]

# plot
fig = plt.figure(figsize=(7, 3))
ax1 = fig.add_subplot(111)
ax1.plot(datetimes, currents, "r.:", label="current")
ax2 = ax1.twinx()
ax2.plot(datetimes, voltages, "b.:", label="voltage")
ax1.grid(True)
ax1.set(title = "randy current consuption @" + str(VOLTAGE) + "V", 
       ylabel="current [mA]")
ax1.legend(loc="center left")
ax2.legend(loc="center right")
ax2.set(ylabel="voltage [V]")
plt.savefig("IDD.png")
sleep(0.1)    
plt.show()
        