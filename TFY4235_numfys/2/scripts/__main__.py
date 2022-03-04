from matplotlib import pyplot as plt

from . import plot

def main():
    d = plot.get_data()#cutoff = -3.e7)
    print(f"Number of particles: {len(d)}")
    plt.hist(d, bins = 100)
    plt.show()

if __name__ == "__main__":
    main()
