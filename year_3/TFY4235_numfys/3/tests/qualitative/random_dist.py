
from nuclear.utils import rng

from matplotlib import pyplot as plt

from typing import Callable


def hist(data, nbins: int = 100, block: bool = True, title: str = ""):
    plt.figure()
    plt.hist(data, bins=nbins)
    if title:
        plt.title(title)
    plt.show(block=block)


def plot_rng(method: Callable[[], int], block: bool = True, title: str = "") -> None:
    d = []
    for _ in range(int(1e6)):
        d.append(method())
    hist(d, block=block, title=title)


def main():
    plot_rng(rng.linear_congruential, block=False, title="Linear Congruential")
    plot_rng(rng.middle_square, block=True, title="Middle Square")
