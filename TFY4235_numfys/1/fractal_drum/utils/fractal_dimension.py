"""Calculate degeneracy and density of states from eigenvalues"""

import numpy as np
from scipy.optimize import curve_fit

def N(omegas: np.ndarray, omega: float) -> int:
    return omegas[omegas < omega].size

def A() -> float:
    return 1.0

def dN(omegas: np.ndarray, omega: float) -> float:
    #omega = np.max(omegas)
    return A()/(4*np.pi)*omega**2 - N(omegas, omega)


def d(omegas: np.ndarray, dNs: np.ndarray) -> float:
    def f(omega, d, k):
        return k*omega**d
    out = curve_fit(f, omegas, dNs)
    return out
