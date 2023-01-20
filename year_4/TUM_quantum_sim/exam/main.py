from TUM_quantum_sim.exam import EXAM_LOGGER as logging

from TUM_quantum_sim import constants as c
from TUM_quantum_sim.exam import potential
from TUM_quantum_sim.exam import plot

import numpy as np
from scipy import sparse as sp


def main():
    logging.info("Starting simulation")

    a = 1e-9
    L = 2*a
    N = 50
    m = c.me
    Vb = c.e0
    n_states = 2

    z = np.linspace(-L/2, L/2, N)
    dz = z[1] - z[0]

    logging.info("Calculating potential")
    V0 = potential.static(z, a, Vb)

    # plot.V(z, V0)

    logging.info(f"Finding {n_states} stationary eigenstates")

    # hamiltonian
    h0 = -c.hbar**2 / (2 * m * dz**2)
    H0 = h0 * sp.diags(
        [1, -2, 1], [-1, 0, 1], 
        shape=(N, N), 
        dtype=np.complex128, 
        format="csc"
        )
    H0 += sp.diags(V0)

    # plot.H(H0)

    # find the smallest (algebraic, not in absolute value) eigenvalues
    _E, _psi = sp.linalg.eigsh(H0, k=n_states, which="SA")
    psi1 = _psi[:, 0]
    psi2 = _psi[:, 1]

    # plot.psi(z, _E, _psi)

    E = 1e9
    omega = np.pi*200e12
    dt = 0.25 * (np.max(V0) + 4 * abs(h0))
    # E = omega = 0

    logging.info(f"{dt = :.2e}")
    logging.info(f"{E = :.2e}")
    logging.info(f"{omega = :.2e}")

    tn = 0
    t_end = 50e-15
    t_store = 0.5e-15 # time between each data storage
    t = [tn]

    V = [V0]

    # calculate initial psi
    psi_half = (psi1 + psi2) * 2**-0.5
    V_half = potential.temporal(z, dt/2, E, omega)
    H_half = dt/(2j * c.hbar) * (H0 + sp.diags(V_half)) @ psi_half
    psi_0 = psi_half - H_half
    psi_1 = psi_half + H_half
    psi = [psi_0]

    logging.info(f"Starting temporal simulation for {t_end / 1e-15 :.1f} ps")
    while tn < t_end:
        
        # Leapfrog
        # psi^n+1 = psi^n-1 + dt*F^n
        # F^n = 1/ihbar * H^n @ psi^n
        # H^n = H0 + V^n

        Vt = potential.temporal(z, tn, E, omega)
        H = dt/(2j * c.hbar) * (H0 + sp.diags(Vt))

        psi_2 = H @ psi_1 + psi_0

        psi_0, psi_1 = psi_1, psi_2

        tn += dt

        # store data every {t_store} seconds
        if tn // t_store > len(psi):
            # approximation
            abs_psi_squared = 0.5 * (np.conjugate(psi_1) * psi_2 + psi_1 * np.conjugate(psi_2))
            psi.append(abs_psi_squared)
            t.append(tn)
            V.append(V0 + Vt)

    t = np.array(t)
    psi = np.array(psi)
    V = np.array(V)
    
    logging.info("Temporal simulation completed")

    # plot.psi2_3D(z, t, psi)

    plot.psi2_animation(z, V, psi)
    

    logging.info("Simulation finished, exiting...")

if __name__ == "__main__":
    main()
