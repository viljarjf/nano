from matplotlib import pyplot as plt
import numpy as np
import os

from . import plot

def main():
    d, t = plot.get_data(n = 10)#cutoff = -3.e7)
    print(f"Number of particles: {len(d)}")
    #plt.plot(np.linspace(0, 1, len(d)), d)
    #for i in range(10):
    #    plt.hist(d[i], bins =300)# np.linspace(0.75, 1, 300))
    U = np.load(os.path.join(os.path.dirname(__file__), "..", "data", "potential.npy"))
    p = [1, 3, 6]
    plt.figure()
    plt.subplot(311)
    for i in p:
        plt.plot(t[i, :], d[i, :])
    plt.legend(p)
    
    plt.subplot(312)
    plt.plot(t[0,:], U[::10,0])
    
    plt.subplot(313)
    plt.plot(t[0,:], U[::10,1])
    plt.show()

if __name__ == "__main__":
    main()
