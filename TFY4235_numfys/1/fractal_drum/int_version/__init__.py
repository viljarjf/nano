"""Version of the code using integers. Less general, more speed"""

from matplotlib import pyplot as plt

from fractal_drum.int_version import lattice

def main():
    a = lattice.generate(6)
    plt.plot(a[0], a[1])
    plt.show()