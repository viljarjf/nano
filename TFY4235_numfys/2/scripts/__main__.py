from matplotlib import pyplot as plt
import numpy as np
import os

import scipy.integrate

from . import plot

def trajectories():
    d, t = plot.get_data(n = 10)#cutoff = -3.e7)
    #plt.plot(np.linspace(0, 1, len(d)), d)
    #for i in range(10):
    #    plt.hist(d[i], bins =300)# np.linspace(0.75, 1, 300))
    U = np.load(os.path.join(os.path.dirname(__file__), "..", "data", "potential.npy"))
    p = [i+10 for i in [1, 3, 6, 11, 12, 13, 14]]
    plt.figure()
    m = 0
    for i in p:
        m = max(m, np.max(d[i,:]))
        plt.plot(t[i, :], d[i, :])

    plt.plot(t[0,:], U[::10,0])
    plt.plot(U[::10,1], t[0,:])
    
    plt.xlabel("Time")
    plt.ylabel("Distance")
    plt.legend(p + ["Potential state", "Potential value"])
    plt.show(block = False)


def hist():
    d, t = plot.get_data()#cutoff = -3.e7)
    
    d += 1
    d %= 1

    plt.figure()
    plt.hist(d[:, -1::10].flatten(), bins=100, density=True)
    p = np.load(os.path.join(os.path.dirname(__file__), "..", "data", "bolzmann.npy"))

    plt.plot(p[:,1], p[:,0])
    print(f"Integral of p: {scipy.integrate.quad(lambda x: p[int(x), 0], 0, len(p))}")
    plt.show()

def main():
    trajectories()
    hist()

if __name__ == "__main__":
    main()
