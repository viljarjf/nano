import matplotlib
import numpy as np
from matplotlib import pyplot as plt
from qm_sim.hamiltonian import Hamiltonian
from qm_sim.spatial_derivative.cartesian import laplacian
from scipy import sparse as sp
from scipy.sparse.linalg import spsolve

from TUM_quantum_sim import constants as c
from TUM_quantum_sim import utils
from TUM_quantum_sim.QCL import QCL_LOGGER as logging
from TUM_quantum_sim.RTD_sim.material import Material
from TUM_quantum_sim.RTD_sim.region import Region
from TUM_quantum_sim.RTD_sim.system import System


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
    return Vb * (-0.25 * (z / z0) ** 2 + 1 / 64 * (z / z0) ** 4) - c.e0 * E * z


def fermi_dirac(E: float, mu: float, T: float) -> float:
    return 1 / (1 + np.exp((E - mu) / (c.kb * T)))


def d_fermi_dirac(E: float, mu: float, T: float) -> float:
    e = np.exp((E - mu) / (c.kb * T))
    return e / (c.kb * T * (1 + e) ** 2)


def DOS_2D(m: float) -> float:
    return m / (np.pi * c.hbar**2)


def calc_n(E: np.ndarray, m: float, mu: float, T: float) -> float:
    return DOS_2D(m) * c.kb * T * sum(fermi_dirac(Ei, mu, T) for Ei in E)


def calc_dn_dmu(E: np.ndarray, m: float, mu: float, T: float) -> float:
    return DOS_2D(m) * c.kb * T * sum(d_fermi_dirac(Ei, mu, T) for Ei in E)


def plot_V(z: np.ndarray, V: np.ndarray):
    plt.figure()
    plt.plot(z * 1e9, V / c.e0)
    plt.xlabel("z [nm]")
    plt.ylabel("V [eV]")
    plt.title("Potential")
    plt.show()


def plot_H(H: sp.spmatrix):
    plt.figure()
    plt.title("Hamiltonian")
    plt.imshow(np.real(H.toarray()))
    plt.show()


def plot_psi(
    z: np.ndarray, V: np.ndarray, En: np.ndarray, psi: np.ndarray, block: bool = True
):
    plt.figure()
    plt.suptitle("$|\Psi|^2$")
    plt.subplot(2, 3, 1)
    plt.plot(z * 1e9, V / c.e0)
    plt.xlabel("z [nm]")
    plt.ylabel("V [eV]")
    plt.title("Potential")
    ax = plt.gca()
    for i in range(min(len(En), 5)):
        plt.subplot(2, 3, i + 2, sharex=ax)
        plt.plot(z * 1e9, abs(psi[i, :]) ** 2)
        plt.title(f"E$_{i}$ = {En[i] / c.e0 :.3e} eV")
        plt.xlabel("z [nm]")
    plt.tight_layout()
    plt.show(block=block)


def plot_rho(z: np.ndarray, nD: np.ndarray, rho: np.ndarray):
    plt.figure()
    plt.subplot(211)
    plt.plot(z, nD)
    plt.title("nD")
    plt.subplot(212)
    plt.plot(z, rho)
    plt.title("$\\rho$")
    plt.tight_layout()
    plt.show()


def main():
    logging.info("Starting simulation")

    matplotlib.use("QtAgg")

    logging.info("Calculating potential")

    AlGaAs = Material(0.15)
    GaAs = Material(0)

    wells = [55, 79, 25, 65, 41, 155, 30, 90, 55]
    regions = []
    prev_width = 0
    materials = [AlGaAs, GaAs]
    current_material = 0
    for width in wells:
        width *= 1e-10  # Å
        regions.append(
            Region(materials[current_material], prev_width, prev_width + width)
        )
        prev_width += width
        current_material ^= 1

    sys = System(regions)

    m = utils.m_star(0)
    E = 1.25e6
    n2D = 3e14
    T = 100
    epsilon = c.ε0 * 12.9

    L = sys.L
    N = int(L / 1e-10)

    z = np.linspace(0, L, N)
    dz = z[1] - z[0]

    sys.set_electric_field(E)
    V = sys.V(z)

    # plot_V(z, V)

    # hamiltonian
    H = Hamiltonian(N, L, m)
    nabla_z2 = laplacian([N], [L]).asformat("csc")

    def iterate(
        V: np.ndarray, log: bool = False
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """returns E, psi, dV, p"""
        if log:
            logging.info("Finding stationary eigenstates")

        H.V = V

        # plot_H(H)

        # find the five smallest (algebraic, not in absolute value) eigenvalues
        En, psi = H.eigen(5)

        if log:
            logging.info("Found 5 stationary eigenstates")
            for i in range(len(En)):
                logging.info(f"E{i} = {En[i] / c.e0 :.3f} eV")

        # plot_psi(z, V, En, psi)

        # estimate mu with newton's method
        # use relative tolerance
        if log:
            logging.info("Estimating mu")
        mu_n = En[0]
        tol = 1e-10
        error = float("inf")
        iter_fun = lambda mu: (calc_n(En, m, mu, T) - n2D) / calc_dn_dmu(En, m, mu, T)
        while error > tol:
            mu_n -= iter_fun(mu_n)
            error = abs(1 - calc_n(En, m, mu_n, T) / n2D)
        mu = mu_n
        if log:
            logging.info(f"mu = {mu / c.e0 :.3e} eV")
        if log:
            logging.info(f"n = {calc_n(En, m, mu, T) :.3e}")
            logging.info(f"n2D = {n2D :.3e}")

        if log:
            logging.info("Calculating occupation")
        p = np.array([calc_n([Ei], m, mu, T) / n2D for Ei in En])
        if log:
            for i in range(len(p)):
                logging.info(f"p{i} = {p[i]*100 :.3f}%")

        if log:
            logging.info("Calculating charge density")

        # dopant concentration
        def dopant_density(z: float) -> float:
            r = sys._find_region(z)
            if r == sys._regions[wells.index(155)]:
                return n2D / (r.end - r.start)
            return 0.0

        nD = np.vectorize(dopant_density)(z)

        rho = c.e0 * (
            nD - n2D * sum([p[i] * abs(psi[i, :]) ** 2 for i in range(len(p))])
        )

        plot_rho(z, nD, rho)

        if log:
            logging.info("Solving the Poisson equation")

        delta_V = c.e0 / (epsilon) * spsolve(nabla_z2, rho)
        # delta_V = delta_V.real # it is strictly real anyway

        return En, psi, delta_V, p

    V0 = V
    En, psi, dV, p = iterate(V0, log=True)
    En_old = 10 * En  # dummy value
    n_iter = 0
    logging.info("Iterating the Schrödinger equation and the Poisson equation")
    while np.any(abs(En - En_old) > 1e-5 * c.e0):
        V = V0 + dV
        En_old = En
        En, psi, dV, p = iterate(V)
        n_iter += 1
        if not n_iter % 10:
            logging.info(f"{n_iter = } iterations")

    logging.info(f"Used {n_iter} iterations")

    En0, psi0, _, p0 = iterate(V0)
    plot_psi(z, V0, En0, psi0, block=False)
    plot_psi(z, V0 + dV, En, psi)

    logging.info("Occupation of initial solution")
    for i in range(len(p0)):
        logging.info(f"p{i} = {p0[i]*100 :.3f}%")
    logging.info(f"Total: {sum(p0)*100:.1f}%")
    logging.info("Occupation of final solution")
    for i in range(len(p)):
        logging.info(f"p{i} = {p[i]*100 :.3f}%")
    logging.info(f"Total: {sum(p)*100:.1f}%")
    logging.info("Energy difference:")
    for i in range(len(p)):
        logging.info(f"delta E{i} = {(En[i] - En0[i]) / c.e0 :.3e} eV")

    logging.info("Simulation finished, exiting...")


if __name__ == "__main__":
    main()
