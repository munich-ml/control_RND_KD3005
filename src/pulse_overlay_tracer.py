# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 11:07:49 2019

@author: holge
"""

from time import sleep
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
from kd3005p import kd3005pInstrument

i_max = 1       # max current [A]
t_step = 0.06    # time step [s]
v_low = 0       # low voltage [V]
v_high = 24     # high voltage [V]
n_prep = 3      # timestep before rise
n_rise = 20     # timesteps in rising edge
n_high = 5     # timesteps at high voltage
n_fall = 20     # timesteps in falling edge
n_low = 5      # timesteps in low voltage

n_total = sum((n_prep, n_rise, n_high, n_fall, n_low))
t_total = n_total * t_step

t = np.linspace(t_step, t_total, n_total)

v = list()
v.extend(n_prep * [v_low])
v.extend(np.linspace(v_low, v_high, n_rise))
v.extend(n_high * [v_high])
v.extend(np.linspace(v_high, v_low, n_fall))
v.extend(n_low * [v_low])


psu = kd3005pInstrument('COM6')

if psu.isConnected:
    print("Connected to " + psu.getIdn())
    psu.setAmp(i_max)
    psu.setVolt(v_low)
    
    fig = plt.figure(figsize=(12,8))
    ax1 = fig.add_subplot(111)
    ax1.plot(t, v, "b.:")
    ax1.grid(True)
    ax2 = ax1.twinx()
    ax1.set(ylabel="voltage [V]", xlabel="time [s]")
    ax2.set(ylabel="current [mA]")
    try:
        for _ in range(50):
            probes = []
            for v_set in v:
                psu.setVolt(v_set)
                sleep(t_step)
                cur = psu.readAmp()
                if cur is None:
                    probes.append(np.nan)
                else:
                    probes.append(float(cur)*1000)
            ax2.plot(t, probes, "r.:")
                        
    except KeyboardInterrupt:
        pass
                            

print("Disconnecting from PowerSupply")
psu.setVolt(0)
psu.close()	
plt.show()
sleep(0.1)    
fig.savefig(dt.datetime.now().strftime("Pulse_overlay_%Y%m%d_%H%M%S.png"))

        