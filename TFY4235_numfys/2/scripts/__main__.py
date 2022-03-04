from matplotlib import pyplot as plt
import numpy as np

from . import plot

def main():
    d = plot.get_data()#cutoff = -3.e7)
    print(f"Number of particles: {len(d)}")
    plt.plot(np.linspace(0, 1, len(d)), d)
    plt.show()

if __name__ == "__main__":
    main()
