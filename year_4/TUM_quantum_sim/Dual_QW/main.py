from TUM_quantum_sim.Dual_QW import DQW_LOGGER

from TUM_quantum_sim import constants as c

from matplotlib import pyplot as plt
import matplotlib
import numpy as np
from scipy import sparse as sp

def potential(
    z: float | np.ndarray,
    a: float,
    Vb: float,
    E: float
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
    z0 = a / (4*2**0.5)
    return Vb * (-0.25 * (z/z0)**2 + 1/64 * (z/z0)**4) - c.e0*E*z

def fermi_dirac(E: float, mu: float, T: float) -> float:
    return 1 / (1 + np.exp((E - mu) / (c.kb * T)))

def d_fermi_dirac(E: float, mu: float, T: float) -> float:
    e = np.exp((E - mu) / (c.kb * T))
    return e / (c.kb * T * (1 + e)**2)

def DOS_2D(m: float) -> float:
    return m / (np.pi*c.hbar**2)

def calc_n(E: np.ndarray, m: float, mu: float, T: float) -> float:
    return DOS_2D(m) * c.kb * T * sum(fermi_dirac(Ei, mu, T) for Ei in E)

def calc_dn_dmu(E: np.ndarray, m: float, mu: float, T: float) -> float:
    return DOS_2D(m) * c.kb * T * sum(d_fermi_dirac(Ei, mu, T) for Ei in E)

def main():
    DQW_LOGGER.info("Starting simulation")

    matplotlib.use("QtAgg")
    
    a = 30e-9
    L = 2*a
    N = 1000
    m = c.me*0.069
    Vb = c.e0
    E = 1e8
    n2D = 3e14
    T = 300

    z = np.linspace(-L/2, L/2, N)
    dz = z[1] - z[0]

    DQW_LOGGER.info("Calculating potential")
    V = potential(z, a, Vb, E)

    # plt.figure()
    # plt.plot(z, V)
    # plt.show()

    DQW_LOGGER.info("Finding stationary eigenstates")
    # hamiltonian
    h0 = -c.hbar**2 / (2 * m * dz**2)
    H0 = h0 * sp.diags([1, -2, 1], [-1, 0, 1], shape=(N, N), dtype=np.complex128, format="csc")
    H0 += sp.diags(V)

    # plt.figure()
    # plt.title("Hamiltonian")
    # plt.imshow(np.real(H0.toarray()))
    # plt.show()

    # find the five smallest (algebraic, not in absolute value) eigenvalues
    En, psi = sp.linalg.eigsh(H0, k=5, which="SA")

    DQW_LOGGER.info("Found 5 stationary eigenstates")
    for i in range(len(En)):
        DQW_LOGGER.info(f"E{i} = {En[i] / c.e0 :.3f} eV")

    # plt.figure()
    # plt.suptitle("$|\Psi_{1,2}|^2$")
    # plt.subplot(2, 1, 1)
    # plt.plot(z, abs(psi[:, 0])**2)
    # plt.title(En[0] / c.e0)
    # plt.subplot(2, 1, 2)
    # plt.plot(z, abs(psi[:, 1])**2)
    # plt.title(En[1] / c.e0)
    # plt.tight_layout()
    # plt.show()
    
    # estimate mu with newton's method
    DQW_LOGGER.info("Estimating mu")
    mu_n = -2.5*c.e0
    tol = c.e0 * 1e-10
    error = float("inf")
    iter_fun = lambda mu: (calc_n(En, m, mu, T) - n2D) / calc_dn_dmu(En, m, mu, T)
    while error > tol:
        error = iter_fun(mu_n)
        mu_n -= error


    DQW_LOGGER.info(f"mu = {mu_n / c.e0 :.3f} eV")
    DQW_LOGGER.info(f"n = {calc_n(En, m, mu_n, T) :.3e}")

    DQW_LOGGER.info("Simulation finished, exiting...")

if __name__ == "__main__":
    main()
