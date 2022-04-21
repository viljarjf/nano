"""Plot stuff"""

from matplotlib import pyplot as plt

def hist(data, nbins: int = 100, block: bool = True):
    plt.hist(data, bins=nbins)
    plt.show(block=block)
