import matplotlib
import numpy as np

from qm_sim.hamiltonian import Hamiltonian
from qm_sim import nature_constants as c
from qm_sim import plot

from TUM_quantum_sim.SQUID import SQUID_LOGGER as logging


def static_potential(
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
        float | np.ndarray: potential [J]
    """
    z0 = a / (4*2**0.5)
    return Vb * (-0.25 * (z/z0)**2 + 1/64 * (z/z0)**4)

def temporal_potential(
    z: float | np.ndarray,
    t: float,
    E: float,
    omega: float
    ) -> float | np.ndarray:
    """Calculate the temporal evolution of the potential

    Args:
        z (float | np.ndarray): position [m]
        t (float): time [s]
        E (float): Electric field strength [V/m]
        omega (float): frequency, [rad/s]

    Returns:
        float | np.ndarray: potential [J]
    """
    return -c.e_0 * E * z * np.sin(omega * t)

def potential(
    z: float | np.ndarray,
    t: float,
    a: float,
    Vb: float,
    E: float,
    omega: float
    ) -> float | np.ndarray:
    """Calculate potential

    Args:
        z (float | np.ndarray): z coordinate in potential, [m]
        t (float): time [s]
        a (float): Potential function parameter, [m]
        Vb (float): Energy scaling, [J]
        E (float): Electric field strength [V/m]
        omega (float): frequency, [rad/s]

    Returns:
        float | np.ndarray: potential [J]
    """
    return static_potential(z, a, Vb) + temporal_potential(z, t, E, omega)

def main():
    logging.info("Starting simulation")

    matplotlib.use("QtAgg")
    
    a = 1e-9
    L = 2*a
    N = 50
    m = c.m_e
    Vb = c.e_0
    E = 1e9
    omega = np.pi*200e12

    logging.info("Initializing Hamiltonian")
    H = Hamiltonian(N, L, m, temporal_scheme="crank-nicolson")
    z, = H.get_coordinate_arrays()
    H.V = lambda t: potential(z, t, a, Vb, E, omega)
    
    H.plot_potential()

    logging.info("Finding stationary eigenstates")
    # find the two smallest (algebraic, not in absolute value) eigenvalues
    _E, _psi = H.eigen(2)
    psi1 = _psi[0, :]
    psi2 = _psi[1, :]

    plot.eigen(_E, _psi)

    logging.info("Starting temporal evolution")
    t_end = 10e-15
    t_store = 0.25e-15 # time between each stored psi
    psi_0 = (psi1 + psi2) / 2**0.5
    
    H.plot_temporal(t_end, t_store, psi_0=psi_0)

    logging.info("Simulation finished, exiting...")

if __name__ == "__main__":
    main()
