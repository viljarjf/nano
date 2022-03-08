from matplotlib import pyplot as plt
import numpy as np

from . import plot

def main():
    d, t = plot.get_data(n = 10)#cutoff = -3.e7)
    print(f"Number of particles: {len(d)}")
    #plt.plot(np.linspace(0, 1, len(d)), d)
    #for i in range(10):
    #    plt.hist(d[i], bins =300)# np.linspace(0.75, 1, 300))

    p = [1, 3, 6]
    for i in p:
        plt.plot(t[i, :], d[i, :])
    plt.legend(p)
    plt.show()

if __name__ == "__main__":
    main()
