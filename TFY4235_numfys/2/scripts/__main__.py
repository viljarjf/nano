from matplotlib import pyplot as plt
import numpy as np

from . import plot

def main():
    d = plot.get_data(n = 10)#cutoff = -3.e7)
    print(f"Number of particles: {len(d)}")
    #plt.plot(np.linspace(0, 1, len(d)), d)
    for i in range(10):
        plt.hist(d[i], bins = 300)#np.linspace(0.75, 1, 300))

    plt.show()

if __name__ == "__main__":
    main()
