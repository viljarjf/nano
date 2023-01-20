
from matplotlib import pyplot as plt
import matplotlib
from matplotlib import cm
from matplotlib.animation import FuncAnimation

import numpy as np
from scipy import sparse as sp

from TUM_quantum_sim import constants as c

## BAD PRACTICE TO RUN CODE ON IMPORT
matplotlib.use("QtAgg")


def V(z: np.ndarray, V: np.ndarray):
    plt.figure()
    plt.plot(z * 1e9, V / c.e0)
    plt.xlabel("z [nm]")
    plt.ylabel("V [eV]")
    plt.title("Potential")
    plt.show()

def H(H: sp.spmatrix):
    plt.figure()
    plt.title("Hamiltonian")
    plt.imshow(np.real(H.toarray()))
    plt.show()

def psi(z: np.ndarray, E: np.ndarray, psi: np.ndarray):
    plt.figure()
    plt.suptitle("$|\Psi_{1,2}|^2$")
    plt.subplot(2, 1, 1)
    plt.plot(z, abs(psi[:, 0])**2)
    plt.title(E[0] / c.e0)
    plt.subplot(2, 1, 2)
    plt.plot(z, abs(psi[:, 1])**2)
    plt.title(E[1] / c.e0)
    plt.tight_layout()
    plt.show()
