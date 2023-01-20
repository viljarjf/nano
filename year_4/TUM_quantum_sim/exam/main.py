from TUM_quantum_sim.SQUID import SQUID_LOGGER as logging

from TUM_quantum_sim import constants as c

from matplotlib import pyplot as plt
import matplotlib
from matplotlib import cm
from matplotlib.animation import FuncAnimation
import numpy as np
from scipy import sparse as sp

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
    return -c.e0 * E * z * np.sin(omega * t)

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
    m = c.me
    Vb = c.e0

    z = np.linspace(-L/2, L/2, N)
    dz = z[1] - z[0]

    logging.info("Calculating potential")
    V0 = static_potential(z, a, Vb)

    # plt.figure()
    # plt.plot(z, V)
    # plt.show()

    logging.info("Finding stationary eigenstates")
    # hamiltonian
    h0 = -c.hbar**2 / (2 * m * dz**2)
    H0 = h0 * sp.diags([1, -2, 1], [-1, 0, 1], shape=(N, N), dtype=np.complex128, format="csc")
    H0 += sp.diags(V0)

    # plt.figure()
    # plt.title("Hamiltonian")
    # plt.imshow(H0.toarray())
    # plt.show()

    # find the two smallest (algebraic, not in absolute value) eigenvalues
    _E, _psi = sp.linalg.eigsh(H0, k=2, which="SA")
    psi1 = _psi[:, 0]
    psi2 = _psi[:, 1]

    # plt.figure()
    # plt.suptitle("$|\Psi_{1,2}|^2$")
    # plt.subplot(2, 1, 1)
    # plt.plot(z, abs(psi1)**2)
    # plt.title(_E[0] / c.e0)
    # plt.subplot(2, 1, 2)
    # plt.plot(z, abs(psi2)**2)
    # plt.title(_E[1] / c.e0)
    # plt.tight_layout()
    # plt.show()


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
        Vt = temporal_potential(z, tn + dt, E, omega)
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
