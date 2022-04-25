"""Plot stuff"""

from matplotlib import pyplot as plt

def hist(data, nbins: int = 100, block: bool = True, title: str = ""):
    plt.figure()
    plt.hist(data, bins=nbins)
    if title:
        plt.title(title)
    plt.show(block=block)
