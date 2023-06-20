import numpy as np
from qm_sim import nature_constants as c
from qm_sim.hamiltonian import Hamiltonian

from TUM_quantum_sim.exam import EXAM_LOGGER as logging
from TUM_quantum_sim.exam import plot, potential


def main():
    logging.info("Starting simulation")

    # simulation setup
    a = 1e-9
    L = 2 * a
    N = 50
    m = c.m_e
    Vb = c.e_0
    n_states = 2
    E = 1e9
    omega = np.pi * 200e12
    t_end = 100e-15  # end of simulation
    t_store = 1e-15  # time between each data storage

    # E = omega = 0       # override

    z = np.linspace(-L / 2, L / 2, N)

    logging.info("Calculating potential")
    V = lambda t: potential.total(z, t, a, Vb, E, omega)

    # Set up hamiltonian
    H = Hamiltonian(N, L, m, temporal_scheme="leapfrog")
    H.V = V

    H.plot_potential()

    logging.info(f"Finding {n_states} stationary eigenstates")

    # find the smallest (algebraic, not in absolute value) eigenvalues
    H.plot_eigen(n_states)

    logging.info("Performing setup for temporal simulation")
    t, psi = H.temporal_evolution(0, t_end, t_store)
    psi = np.abs(psi**2)

    _V = []
    for ti in t:
        _V.append(H.V(ti))
    V = np.array(_V)

    logging.info("Temporal simulation completed")

    plot.psi2_3D(z, t, psi)

    plot.psi2_animation(z, V, psi)

    logging.info("Simulation finished, exiting...")


if __name__ == "__main__":
    main()
