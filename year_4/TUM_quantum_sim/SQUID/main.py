from TUM_quantum_sim.SQUID import SQUID_LOGGER

from TUM_quantum_sim import constants as c

from matplotlib import pyplot as plt
import matplotlib
import numpy as np
from scipy import sparse as sp

def potential(
    z: float | np.ndarray,
    a: float,
    Vb: float
    ) -> np.ndarray:
    """create a discretised array of the potential

    Args:
        z (float | np.ndarray): z coordinate in potential, [m]
        a (float): Potential function parameter, [m]
        Vb (float): Energy scaling, [J]

    Returns:
        np.ndarray: array of potential values
    """
    z0 = a / (4*2**0.5)
    return Vb * (-0.25 * (z/z0)**2 + 1/64 * (z/z0)**4)

def main():
    SQUID_LOGGER.info("Starting simulation")

    matplotlib.use("QtAgg")
    
    a = 1e-9
    L = 2*a
    N = 50
    m = c.me
    Vb = c.e0

    z = np.linspace(-L/2, L/2, N)
    dz = z[1] - z[0]

    SQUID_LOGGER.info("Calculating potential")
    V = potential(z, a, Vb)

    # plt.figure()
    # plt.plot(z, V)
    # plt.show()

    SQUID_LOGGER.info("Finding stationary eigenstates")
    # hamiltonian
    H = (c.hbar**2 / (2 * m)) * sp.diags([-1, 1, -1], [-1, 0, 1], shape=(N, N)) + sp.diags(V)
    E, psi = sp.linalg.eigsh(H, k=2, which="SA")

    plt.figure()
    plt.title("$\Psi_{1,2}$")
    plt.subplot(2, 1, 1)
    plt.plot(z, psi[:, 0])
    plt.title(E[0] / c.e0)
    plt.subplot(2, 1, 2)
    plt.plot(z, psi[:, 1])
    plt.title(E[1] / c.e0)
    plt.show()



    SQUID_LOGGER.info("Simulation finished, exiting...")

if __name__ == "__main__":
    main()
