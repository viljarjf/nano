from TUM_quantum_sim.SQUID import SQUID_LOGGER

from TUM_quantum_sim import constants as c

from matplotlib import pyplot as plt
import matplotlib
from matplotlib import cm
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
    V = static_potential(z, a, Vb)

    # plt.figure()
    # plt.plot(z, V)
    # plt.show()

    SQUID_LOGGER.info("Finding stationary eigenstates")
    # hamiltonian
    h0 = -c.hbar**2 / (2 * m * dz**2)
    H0 = h0 * sp.diags([1, -2, 1], [-1, 0, 1], shape=(N, N))
    H = H0 + sp.diags(V)

    # plt.figure()
    # plt.title("Hamiltonian")
    # plt.imshow(H.toarray())
    # plt.show()

    # find the two smallest (algebraic, not in absolute value) eigenvalues
    _E, _psi = sp.linalg.eigsh(H, k=2, which="SA")
    psi1 = _psi[:, 0]
    psi2 = _psi[:, 1]

    # plt.figure()
    # plt.suptitle("$\Psi_{1,2}$")
    # plt.subplot(2, 1, 1)
    # plt.plot(z, psi1)
    # plt.title(_E[0] / c.e0)
    # plt.subplot(2, 1, 2)
    # plt.plot(z, psi2)
    # plt.title(_E[1] / c.e0)
    # plt.tight_layout()
    # plt.show()


    # Crank-Nicholson
    # psi^n+1 = psi^n + dt/2 * (F^n + F^n+1)
    # F^n = 1/ihbar * H^n * psi^n
    # Rearrange this by hand to get the stuff in the while loop
    t = []
    tn = 0
    t_end = 10e-15
    t.append(tn)
    dt = 0.5 * (np.max(V) + 4 * abs(h0))

    E = 1e9
    omega = np.pi*2e12
    E = omega = 0


    SQUID_LOGGER.info(f"{dt = :.2e}")
    SQUID_LOGGER.info(f"{E = :.2e}")
    SQUID_LOGGER.info(f"{omega = :.2e}")

    psi = []
    psi0 = (psi1 + psi2) * 2**-0.5
    psi_n = psi0
    psi.append(psi_n)

    prefactor = dt/(2j * c.hbar)
    while tn < t_end:
        Vn = potential(z, tn + dt, a, Vb, E, omega)
        Hn = H0 + sp.diags(Vn)

        # just fix this, its wrong in the notes I think
        psi_n = sp.linalg.inv(sp.eye(N, N) - prefactor * Hn) @ (psi_n + prefactor * H)

        tn += dt
        H = Hn

        # store every 1fs
        if tn // 1e-15 > len(psi):
            psi.append(psi_n)
            t.append(tn)
            SQUID_LOGGER.info(f"{tn = :.2e}")
    t = np.array(t)
    psi = np.array(psi)

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    # Make data.
    X, Y = np.meshgrid(z, t)

    # Plot the surface.
    surf = ax.plot_surface(X, Y, psi, cmap=cm.get_cmap("viridis"),linewidth=0, antialiased=False)
    plt.xlabel("z [m]")
    plt.ylabel("t [s]")

    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()

    SQUID_LOGGER.info("Simulation finished, exiting...")

if __name__ == "__main__":
    main()
