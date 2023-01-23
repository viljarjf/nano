
import matplotlib
import numpy as np
from matplotlib import cm
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
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

def H(H: np.ndarray):
    plt.figure()
    plt.title("Hamiltonian")
    plt.imshow(np.real(H))
    plt.show()

def psi(z: np.ndarray, E: np.ndarray, psi: np.ndarray):
    plt.figure()
    plt.title("$|\Psi_{1,2}|^2$")
    plt.plot(z / 1e-9, abs(psi[0, :])**2)
    plt.plot(z / 1e-9, abs(psi[1, :])**2)
    plt.xlabel("z [nm]")
    plt.legend([
        f"E$_1$: {E[0] / c.e0 :.3f} eV",
        f"E$_2$: {E[1] / c.e0 :.3f} eV"
        ])
    plt.tight_layout()
    plt.show()

def psi2_3D(z: np.ndarray, t: np.ndarray, abs_psi_squared: np.ndarray):
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    X, Y = np.meshgrid(z / 1e-9, t / 1e-15)
    surf = ax.plot_surface(
        X, Y, abs_psi_squared, 
        cmap=cm.get_cmap("viridis"),
        linewidth=0, 
        antialiased=False
        )
    plt.xlabel("z [nm]")
    plt.ylabel("t [fs]")
    plt.title("$|\Psi|^2$")
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()

def psi2_animation(z: np.ndarray, V: np.ndarray, abs_psi_squared: np.ndarray):
    fig, (ax1, ax2) = plt.subplots(2, 1)

    ln_psi, = ax1.plot(z / 1e-9, abs_psi_squared[0, :])
    ln_V, = ax2.plot(z / 1e-9, V[0, :] / c.e0)

    def init():
        ax1.set_title("$|\Psi|^2$")
        ax1.set_xlabel("z [nm]")
        ax2.set_title("Potential [eV]")
        ax2.set_xlabel("z [nm]")
        ax1.set_ylim(0, np.max(abs_psi_squared) * 1.1)
        ax2.set_ylim(np.min(V / c.e0), np.max(V / c.e0))
        fig.tight_layout()
        return ln_psi, ln_V,

    def frames():
        for n in range(abs_psi_squared.shape[0]):
            yield abs_psi_squared[n, :], V[n, :]

    def update(data):
        ln_psi.set_data(z / 1e-9, data[0])
        ln_V.set_data(z / 1e-9, data[1] / c.e0)
        return ln_psi, ln_V,

    ani = FuncAnimation(fig, update, frames=frames, init_func=init, blit=True)
    plt.show()

def psi2_z(t: np.ndarray, z_ind: int, abs_psi_squared: np.ndarray):
    plt.figure()
    plt.plot(t / 1e-15, abs_psi_squared[:, z_ind])
    plt.xlabel("time [fs]")
    plt.ylabel(f"$|\psi_{{{int(z_ind)}}}|^2$")
    plt.show()