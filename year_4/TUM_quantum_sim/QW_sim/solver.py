from scipy import sparse as sp
import numpy as np

from TUM_quantum_sim.QW_sim.system import System

from qm_sim.hamiltonian import Hamiltonian

from dataclasses import dataclass

@dataclass
class Solution:
    eigenvalue: float | complex
    eigenvector: np.ndarray


def eigen(sys: System, H: Hamiltonian, n: int = 5) -> list[Solution]:
    vals, vecs = H.eigen(n)

    out = []
    for i in range(n):
        out.append(
            Solution(
                vals[i],
                vecs[i, :]
            )
        )
    return out
