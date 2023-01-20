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

    # Crank-Nicholson
    # psi^n+1 = psi^n + dt/2 * (F^n + F^n+1)
    # F^n = 1/ihbar * H^n @ psi^n
    # H^n = H0 + V^n
    # Rearrange this by hand to get the stuff in the while loop
    tn = 0
    t = [tn]
    t_end = 10e-15
    t_store = 0.25e-15 # time between each stored psi
    dt = 0.25 * (np.max(V0) + 4 * abs(h0))

    E = 1e9
    omega = np.pi*200e12
    # E = omega = 0


    logging.info(f"{dt = :.2e}")
    logging.info(f"{E = :.2e}")
    logging.info(f"{omega = :.2e}")

    psi_n = (psi1 + psi2) * 2**-0.5
    psi = [psi_n]

    V = [V0]

    I = sp.eye(N, N, format="csc")
    prefactor = dt/(2j * c.hbar)
    H = prefactor * H0

    while tn < t_end:
        Vt = potential.temporal(z, tn + dt, E, omega)
        Hn = prefactor * (H0 + sp.diags(Vt))

        psi_n = sp.linalg.inv(I - Hn) @ (I + H) @ psi_n

        tn += dt
        H = Hn

        # store every 1fs
        if tn // t_store > len(psi):
            psi.append(psi_n)
            t.append(tn)
            V.append(V0 + Vt)
            logging.info(f"{tn = :.2e}")

    t = np.array(t)
    psi = np.array(psi)
    V = np.array(V)

    return
    # 3D plot
    # fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    # X, Y = np.meshgrid(z, t)
    # surf = ax.plot_surface(X, Y, abs(psi)**2, cmap=cm.get_cmap("viridis"),linewidth=0, antialiased=False)
    # plt.xlabel("z [m]")
    # plt.ylabel("t [s]")
    # plt.title("$|\Psi|^2$")
    # fig.colorbar(surf, shrink=0.5, aspect=5)
    # plt.show()

    # animation
    fig, (ax1, ax2) = plt.subplots(2, 1)
    ln_psi, = ax1.plot(z, abs(psi[0, :])**2)
    ln_V, = ax2.plot(z, V[0, :])

    def init():
        ax1.set_ylim(0, 0.2)
        ax2.set_ylim(-2*c.e0, 10*c.e0)
        return ln_psi, ln_V,

    def frames():
        for n in range(psi.shape[0]):
            yield psi[n, :], V[n, :]

    def update(data):
        ln_psi.set_data(z, abs(data[0])**2)
        ln_V.set_data(z, data[1])
        return ln_psi, ln_V,

    ani = FuncAnimation(fig, update, frames=frames, init_func=init, blit=True)
    plt.show()

    logging.info("Simulation finished, exiting...")

if __name__ == "__main__":
    main()
