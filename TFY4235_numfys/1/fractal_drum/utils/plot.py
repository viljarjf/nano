"""Create beautiful plots"""

from matplotlib import pyplot as plt
import os
import numpy as np

def eigenmodes(n: int, eigenvectors: np.ndarray, eigenvals: np.ndarray, boundary: np.ndarray):
    figdir = os.path.join(os.path.dirname(__file__), "..", "..", "figures")
    if not os.path.exists(figdir):
        os.makedirs(figdir)

    x = np.arange(0, n)
    y = np.arange(0, n)
    for i in range(eigenvectors.shape[1]):
        plt.figure(figsize = (6, 6), dpi = 250)
        plt.title(f"omega / v: {eigenvals[i]:.5f}")
        plt.pcolormesh(x, y, eigenvectors[:, i].reshape(n, n))
        plt.plot([*boundary[0, :], boundary[0, -1]], [*boundary[1, :], boundary[1, -1]] )
        plt.colorbar()
        plt.xticks([])
        plt.yticks([])
        plt.savefig(os.path.join(figdir, f"Eigenvector #{i+1:03}.png"))
        plt.close()

def is_inside(grid: np.ndarray):
    n = grid.shape[0]
    x = np.arange(0, n)
    y = np.arange(0, n)
    plt.figure(figsize = (6, 6), dpi = 250)
    plt.pcolormesh(x, y, grid)
    plt.title(f"Result of `is_inside`")
    plt.colorbar()
    plt.xticks([])
    plt.yticks([])
    plt.show()
