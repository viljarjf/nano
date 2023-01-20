
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

def psi_3D(z: np.ndarray, t: np.ndarray, psi: np.ndarray):
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    X, Y = np.meshgrid(z, t)
    surf = ax.plot_surface(X, Y, abs(psi)**2, cmap=cm.get_cmap("viridis"),linewidth=0, antialiased=False)
    plt.xlabel("z [m]")
    plt.ylabel("t [s]")
    plt.title("$|\Psi|^2$")
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()

def psi_animation(z: np.ndarray, V: np.ndarray, psi: np.ndarray):
    fig, (ax1, ax2) = plt.subplots(2, 1)

    ln_psi, = ax1.plot(z, abs(psi[0, :])**2)
    ln_V, = ax2.plot(z, V[0, :])

    def init():
        ax1.set_title("$|\Psi|^2$")
        ax2.set_title("Potential [eV]")
        ax1.set_ylim(0, 0.2)
        ax2.set_ylim(-2, 10)
        fig.tight_layout()
        return ln_psi, ln_V,

    def frames():
        for n in range(psi.shape[0]):
            yield psi[n, :], V[n, :]

    def update(data):
        ln_psi.set_data(z, abs(data[0])**2)
        ln_V.set_data(z, data[1] / c.e0)
        return ln_psi, ln_V,

    ani = FuncAnimation(fig, update, frames=frames, init_func=init, blit=True)
    plt.show()