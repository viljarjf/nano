
from nuclear.utils import rng, plot

def plot_rng(method: "function", block: bool = True, title: str = "") -> None:
    d = []
    for _ in range(int(1e6)):
        d.append(method())
    plot.hist(d, block=block, title=title)

def main():
    plot_rng(rng.linear_congruential, block=False, title="Linear Congruential")
    plot_rng(rng.middle_square, block=True, title="Middle Square")
