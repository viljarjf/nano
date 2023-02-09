import matplotlib
import numpy as np
from matplotlib import pyplot as plt
from scipy.integrate import solve_ivp

from TUM_quantum_sim import constants as c
from TUM_quantum_sim.QB import QB_LOGGER as logging


a = 0
b = 1


def d_rho_coll_fun(rho: np.ndarray, rho_eq: np.ndarray, g: np.ndarray) -> np.ndarray:
    return -g * (rho - rho_eq)


def d_rho_fun(H: np.ndarray, rho: np.ndarray) -> np.ndarray:
    return 1 / (1j*c.hbar) * (H @ rho - rho @ H)
    

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
    Omega_R = 0.05 * omega_0

    H0 = np.array([[E_g, 0], [0, 0]])
    HI = lambda t: -c.hbar * Omega_R * np.cos(omega_0 * t)
    H = lambda t: H0 + HI(t)

    logging.info("Finding non-dissipated equilibrium")
    
    def equilibrium_ode_fun(t, y): 
        _H = H(t)
        _y = y.reshape(2,2)
        return d_rho_fun(_H, _y).flatten()

    y0 = np.array([[0, 1], [1, 0]]).flatten().astype(np.complex128)
    T = 5*np.pi / Omega_R

    sol_eq = solve_ivp(equilibrium_ode_fun, [0, T], y0)

    rho_eq = sol_eq.y[:, 1].reshape(2,2)
    print(rho_eq)
    rho_eq[1, 0] = 0
    rho_eq[0, 1] = 0

    def dissipation_ode_fun(t, y):
        _H = H(t)
        _y = y.reshape(2,2)
        out = d_rho_fun(_H, _y) + d_rho_coll_fun(_y, rho_eq, g)
        return out.flatten()

    sol_diss = solve_ivp(dissipation_ode_fun, [0, T], y0)

    print(sol_diss.y[:, 1].reshape(2,2))

    logging.info("Simulation finished, exiting...")
