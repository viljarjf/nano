"""Create beautiful plots"""

from matplotlib import pyplot as plt
import matplotlib
import numpy as np
import gc

from fractal_drum.utils import __config as cfg

def eigenmodes(n: int, eigenvectors: np.ndarray, eigenvals: np.ndarray, boundary: np.ndarray, amount: int = 100):

    matplotlib.use('agg')
    x = np.arange(0, n)
    y = np.arange(0, n)
    vmax = np.max(np.abs(eigenvectors[:, :min(eigenvectors.shape[1], amount)]))
    vmin = -vmax
    for i in range(min(eigenvectors.shape[1], amount)):
        f = plt.figure(figsize = (6, 6), dpi = 250)
        plt.title(f"omega / v: {eigenvals[i]:.5f}")
        plt.pcolormesh(x, y, eigenvectors[:, i].reshape(n, n))#, vmin=vmin, vmax=vmax)
        plt.plot([*boundary[0, :], boundary[0, -1]], [*boundary[1, :], boundary[1, -1]] )
        plt.colorbar()
        plt.xticks([])
        plt.yticks([])
        plt.tight_layout()
        plt.savefig(cfg.figure_filepath(f"Eigenvector #{i+1:03}.png"))

        # matplotlib memory leak "fix"
        plt.cla()
        plt.clf()
        plt.close(f)
        plt.close("all")
        gc.collect

def is_inside(grid: np.ndarray):
    n = grid.shape[0]
    x = np.arange(0, n)
    y = np.arange(0, n)
    matplotlib.use('tkagg')
    plt.figure(figsize=(6, 6), dpi=250)
    plt.pcolormesh(x, y, grid)
    plt.title(f"Result of `is_inside`")
    plt.colorbar()
    plt.xticks([])
    plt.yticks([])
    plt.show()


def idos(omegas: np.ndarray, Ns: np.ndarray):
    matplotlib.use('tkagg')
    plt.figure()
    plt.plot(omegas, Ns)
    plt.xlabel("$\omega$")
    plt.ylabel("$N(\omega)$")
    plt.show()

def weyl_berry_conjecture(omegas: np.ndarray, dNs: np.ndarray, d, k):
    matplotlib.use('tkagg')
    plt.figure()
    plt.title("Fractal dimension analysis")
    plt.plot(omegas, dNs)
    plt.plot(omegas, k*omegas**d, "-")
    #plt.xscale("log")
    #plt.yscale("log")
    plt.xlabel("$\omega$")
    plt.ylabel("$\Delta N(\omega)$")
    plt.show()