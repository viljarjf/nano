import matplotlib
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.integrate import solve_ivp

from TUM_quantum_sim import constants as c
from TUM_quantum_sim.QB import QB_LOGGER as logging


a = 0
b = 1

def d_rho_coll_func(rho: np.ndarray, rho_eq: np.ndarray, g: np.ndarray) -> np.ndarray:
    return -g * (rho - rho_eq)

def d_rho_func(H: np.ndarray, rho: np.ndarray) -> np.ndarray:
    return 1 / (1j*c.hbar) * (H @ rho - rho @ H)
    
def bloch_vector_func(rho: np.ndarray) -> np.ndarray:
    """Calculate the bloch vector from a density matrix.
    Cartesian coordinates

    Args:
        rho (np.ndarray): shape(2, 2, n) for n density matrices

    Returns:
        np.ndarray: shape(3, n), xyz coordinates
    """
    rho_aa = rho[a, a, :]
    rho_ba = rho[b, a, :]
    x = 2.0 * rho_ba.real
    y = 2.0 * rho_ba.imag
    z = 2.0 * rho_aa - 1.0
    return np.array([x, y, z])

def bloch_vector_animation(s: np.ndarray):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection="3d")
    q = ax.quiver(0, 0, 0, *s[:, 0].real)
    path, = ax.plot3D(*s[:, 0].real)
    artists = [path, q]

    def init():
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
        ax.set_zlim(-1, 1)
        return artists

    def frames():
        for n in range(s.shape[1]):
            yield n, (0, 0, 0, *s[:, n].real)

    def update(data):
        n, vec = data
        # update path
        artists[0].set_data_3d(*s[:, :n].real)
        # update vector
        artists[-1].remove()
        artists.pop()
        artists.append(ax.quiver(*vec))
        return artists

    ani = FuncAnimation(fig, update, frames=frames, init_func=init, interval=1)
    plt.show()

def main():
    matplotlib.use("QtAgg")

    logging.info("Starting simulation")

    # dipole matrix
    _d = 0.5e-9*c.e0
    d = np.array([[0, _d], [_d, 0]])
    # relaxation rates
    g_1 = 0
    g_2 = 2e13 
    g = np.array([[g_1, g_2], [g_2, g_1]])
    # energy gap
    E_g = 1.43*c.e0
    # energy and frequency of external wave
    omega_0 = E_g / c.hbar
    Omega_R = 1 * omega_0

    H0 = np.array([[E_g, 0], [0, 0]])
    HI = lambda t: -c.hbar * Omega_R * np.cos(omega_0 * t)
    H = lambda t: H0 + HI(t)

    logging.info("Finding non-dissipated equilibrium")
    
    def equilibrium_ode_func(t, y): 
        _H = H(t)
        _y = y.reshape(2,2)
        return d_rho_func(_H, _y).flatten()

    y0 = np.array([[0, 1], [1, 0]]).flatten().astype(np.complex128)
    T = 5*np.pi / Omega_R

    sol_eq = solve_ivp(equilibrium_ode_func, [0, T], y0)

    rho_eq = sol_eq.y[:, 1].reshape(2,2).copy()
    rho_eq[1, 0] = 0
    rho_eq[0, 1] = 0

    print(rho_eq)

    def dissipation_ode_func(t, y):
        _H = H(t)
        _y = y.reshape(2,2)
        out = d_rho_func(_H, _y) + d_rho_coll_func(_y, rho_eq, g)
        return out.flatten()
    
    t = np.linspace(0, T, 1000)
    sol_diss = solve_ivp(dissipation_ode_func, [0, T], y0, t_eval=t)

    rho = sol_diss.y.reshape(2,2, -1).copy()
    
    s = bloch_vector_func(rho)
    bloch_vector_animation(s)

    plt.figure()


    logging.info("Simulation finished, exiting...")
