from TUM_quantum_sim.exam import EXAM_LOGGER as logging

from TUM_quantum_sim import constants as c
from TUM_quantum_sim.exam import potential
from TUM_quantum_sim.exam import plot
from TUM_quantum_sim.exam.sparse_override import Hamiltonian

import numpy as np
from scipy import sparse as sp


def main():
    logging.info("Starting simulation")

    # simulation setup
    a = 1e-9
    L = 2*a
    N = 50
    m = c.me
    Vb = c.e0
    n_states = 2
    E = 1e9
    omega = np.pi*200e12
    t_end = 100e-15     # end of simulation
    t_store = 1e-15     # time between each data storage

    # E = omega = 0       # override 

    z = np.linspace(-L/2, L/2, N)
    dz = z[1] - z[0]

    logging.info("Calculating potential")
    V0 = potential.static(z, a, Vb)

    plot.V(z, V0)

    logging.info(f"Finding {n_states} stationary eigenstates")

    # Set up hamiltonian
    h0 = -c.hbar**2 / (2 * m * dz**2)
    H0 = Hamiltonian(sp.diags(
        [h0, -2*h0, h0], [-1, 0, 1], 
        shape=(N, N), 
        dtype=np.complex128, 
        format="dia"
        ))
    H0.add_static_potential(V0)

    plot.H(H0)

    # find the smallest (algebraic, not in absolute value) eigenvalues
    _E, _psi = sp.linalg.eigsh(H0, k=n_states, which="SA")
    # normalise
    for i in range(n_states):
        _psi[:, i] /= np.sqrt(np.trapz(_psi[:, i]**2, z))

    logging.info("Eigenstates found.")
    plot.psi(z, _E, _psi)

    logging.info("Performing setup for temporal simulation")
    # estimate a decent dt from lectures
    V_max = V0 + potential.temporal(z, np.pi/2, E, 1)
    E_max = max(
        abs(min(V_max)),
        abs(max(V_max) + 4 * abs(h0)),
        )
    dt = 0.5 * c.hbar / E_max
    logging.info(f"{dt = :.2e} s")

    # calculate initial psi
    psi_half = (_psi[:, 0] + _psi[:, 1]) * 2**-0.5
    V_half = potential.temporal(z, dt/2, E, omega)
    H_half = H0.add(V_half) @ (dt/(2j * c.hbar) * psi_half)
    psi_0 = psi_half - H_half
    psi_1 = psi_half + H_half
    psi = [np.abs(psi_0)**2]

    tn = 0      # current simulation time
    t = [tn]    # array for storing times
    V = [V0]    # array for storing potentials

    logging.info(f"Starting temporal simulation for {t_end / 1e-15 :.1f} fs")
    coef = 2*dt/(1j * c.hbar)
    steps = 0
    while tn < t_end:
        steps += 1

        # Leapfrog
        # psi^n+1 = psi^n-1 + 2*dt*F^n
        # F^n = 1/ihbar * H^n @ psi^n
        # H^n = H0 + V^n

        Vt = potential.temporal(z, tn, E, omega)

        psi_2 = H0.add(Vt) @ (coef * psi_1) + psi_0

        psi_0, psi_1 = psi_1, psi_2

        tn += dt

        # store data every {t_store} seconds
        if tn // t_store > len(psi):
            # approximation
            abs_psi_squared = 0.5 * (np.conjugate(psi_1) * psi_2 + psi_1 * np.conjugate(psi_2))
            psi.append(abs_psi_squared.real) # it's strictly real anyway, just make matplotlib happy
            t.append(tn)
            V.append(V0 + Vt)

    t = np.array(t)
    psi = np.array(psi)
    V = np.array(V)
    
    logging.info("Temporal simulation completed")
    logging.info(f"Took {steps} steps, stored data {len(t)} times")

    plot.psi2_3D(z, t, psi)

    plot.psi2_animation(z, V, psi)
    
    # plot.psi2_z(t, np.nonzero(z == 0.0)[0], psi)

    logging.info("Simulation finished, exiting...")

if __name__ == "__main__":
    main()
