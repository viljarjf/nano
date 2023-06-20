import logging

import matplotlib
import numpy as np
from matplotlib import pyplot as plt
from qm_sim import nature_constants as c
from qm_sim.hamiltonian import Hamiltonian

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
)


def potential(
    z: float | np.ndarray, a: float, Vb: float, E: float
) -> float | np.ndarray:
    """Calculate potential

    Args:
        z (float | np.ndarray): z coordinate in potential, [m]
        a (float): Potential function parameter, [m]
        Vb (float): Energy scaling, [J]
        E (float): Electric field strength [V/m]

    Returns:
        float | np.ndarray: potential [J]
    """
    z0 = a / (4 * 2**0.5)
    return Vb * (-0.25 * (z / z0) ** 2 + 1 / 64 * (z / z0) ** 4) - c.e_0 * E * z


def fermi_dirac(E: float, mu: float, T: float) -> float:
    return 1 / (1 + np.exp((E - mu) / (c.k_b * T)))


def d_fermi_dirac(E: float, mu: float, T: float) -> float:
    e = np.exp((E - mu) / (c.k_b * T))
    return e / (c.k_b * T * (1 + e) ** 2)


def DOS_2D(m: float) -> float:
    return m / (np.pi * c.h_bar**2)


def calc_n(E: np.ndarray, m: float, mu: float, T: float) -> float:
    return DOS_2D(m) * c.k_b * T * sum(fermi_dirac(Ei, mu, T) for Ei in E)


def calc_dn_dmu(E: np.ndarray, m: float, mu: float, T: float) -> float:
    return DOS_2D(m) * c.k_b * T * sum(d_fermi_dirac(Ei, mu, T) for Ei in E)


def main():
    logging.info("Starting simulation")

    matplotlib.use("QtAgg")

    a = 30e-9
    L = 2 * a
    N = 1000
    m = c.m_e * 0.069
    Vb = c.e_0
    E = 1e8
    n2D = 3e14
    T = 300

    z = np.linspace(-L / 2, L / 2, N)

    logging.info("Calculating potential")
    V = potential(z, a, Vb, E)

    plt.figure()
    plt.plot(z, V)
    plt.show()

    logging.info("Finding stationary eigenstates")
    # hamiltonian
    H0 = Hamiltonian((N,), (L,), m)
    H0.V = V

    plt.figure()
    plt.title("Hamiltonian")
    plt.imshow(np.real(H0.asarray()))
    plt.show()

    # find the five smallest (algebraic, not in absolute value) eigenvalues
    En, psi = H0.eigen(5)

    logging.info("Found 5 stationary eigenstates")
    for i in range(len(En)):
        logging.info(f"E{i} = {En[i] / c.e_0 :.3f} eV")

    plt.figure()
    plt.suptitle("$|\\Psi_{1,2}|^2$")
    plt.subplot(2, 1, 1)
    plt.plot(z, abs(psi[0, :]) ** 2)
    plt.title(En[0] / c.e_0)
    plt.subplot(2, 1, 2)
    plt.plot(z, abs(psi[1, :]) ** 2)
    plt.title(En[1] / c.e_0)
    plt.tight_layout()
    plt.show()

    # estimate mu with newton's method
    logging.info("Estimating mu")
    mu_n = -2.5 * c.e_0
    tol = c.e_0 * 1e-10
    error = float("inf")
    iter_fun = lambda mu: (calc_n(En, m, mu, T) - n2D) / calc_dn_dmu(En, m, mu, T)
    while error > tol:
        error = iter_fun(mu_n)
        mu_n -= error

    logging.info(f"mu = {mu_n / c.e_0 :.3f} eV")
    logging.info(f"n = {calc_n(En, m, mu_n, T) :.3e}")

    logging.info("Simulation finished, exiting...")


if __name__ == "__main__":
    main()
