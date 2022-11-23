
import numpy as np

from RTD_sim.system import System
from RTD_sim.transfer_matrix import Td, TransferMatrix

def _T_mat_tot(E: float, sys: System, N: int) -> TransferMatrix:
    z = np.linspace(0, sys.L, N)
    k1 = sys.k(E, 0)
    T_final = np.eye(2)
    for i in z:
        k2 = sys.k(E, i)
        T_final = T_final @ Td(k1, k2, i)
    return T_final

def T(E: float, sys: System, N: int):
    T_mat = _T_mat_tot(E, sys, N)
    beta0 = sys.beta(E, 0)
    betaN = sys.beta(E, sys.L)
    return betaN / beta0 * (np.linalg.det(T_mat) / T_mat[1,1])**2
