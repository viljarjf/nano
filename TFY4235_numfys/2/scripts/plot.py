"""Pretty plots"""

import os
import numpy as np
from matplotlib import pyplot as plt
import scipy.integrate

from . import data

def trajectories(block = True, all = False, legend = True):
    d = data.get("particles")#cutoff = -3.e7)
    t = data.get("time")

    p = [i+10 for i in [1]]#, 3, 6, 11, 12, 13, 14]]
    if all:
        p = list(range(d.shape[0]))
    plt.figure()
    m = 0
    for i in p:
        m = max(m, np.max(d[i,:]))
        plt.plot(t, d[i, :])

    #U = data.get("potential.npy")
    #plt.plot(t, U[::10,0])
    #plt.plot(U[::10,1], t)
    
    plt.xlabel("Time")
    plt.ylabel("Distance")
    if legend:
        plt.legend(p + ["Potential state", "Potential value"])
    plt.show(block = block)


def hist(block = True):
    d, t = data.get_data()#cutoff = -3.e7)
    
    d += 1
    d %= 1

    plt.figure()
    plt.hist(d[:, -1::10].flatten(), bins=100, density=True)
    p = data.get("bolzmann.npy")

    plt.plot(p[:,1], p[:,0])
    print(f"Integral of p: {scipy.integrate.quad(lambda x: p[int(x), 0], 0, len(p))}")
    plt.show(block = block)

def drift_velocities(v: np.ndarray, title = None, block = True): 
    tau = data.get("tau")
    tau_unique = np.unique(tau)
    v_reshape = np.reshape(v, (tau_unique.shape[0], -1))
    v_reshape_mean = np.mean(v_reshape, axis = 1)
    v_reshape_std = np.std(v_reshape, axis = 1)
    plt.figure()
    if title is not None:
        plt.title(title)
    plt.errorbar(tau_unique, v_reshape_mean, yerr=v_reshape_std)
    plt.xlabel("Tau")
    plt.ylabel("Velocity")
    plt.title("Mean")
    
    plt.show(block=block)
