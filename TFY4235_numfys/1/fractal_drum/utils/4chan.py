"""Calculate degeneracy and density of states from eigenvalues"""

import numpy as np

def N(omegas: np.ndarray, omega: float) -> int:
    return omegas[omegas < omega].size


def IDOS(omegas: np.ndarray, omega: float) -> float:
    pass
