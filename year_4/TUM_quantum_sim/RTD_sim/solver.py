
import numpy as np

from TUM_quantum_sim.RTD_sim.system import System
from TUM_quantum_sim.RTD_sim.transfer_matrix import M, TransferMatrix


def _T_mat_tot(E: float, sys: System, N: int) -> TransferMatrix:
    z = np.linspace(0, sys.L, N)
    dz = sys.L / N
    T_final = np.eye(2, dtype=np.complex128)
    for i in range(N-1):
        k = sys.k(E, z[i])
        beta1 = sys.beta(E, z[i])
        beta2 = sys.beta(E, z[i+1])
        T_final = M(k, beta1, beta2, dz) @ T_final
    return T_final

def T(E: float, sys: System, N: int):
    T_mat = _T_mat_tot(E, sys, N)
    beta0 = sys.beta(E, 0)
    betaN = sys.beta(E, sys.L)
    return betaN / beta0 * np.abs(np.linalg.det(T_mat) / T_mat[1,1])**2
