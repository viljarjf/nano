from dataclasses import dataclass

import numpy as np
from qm_sim.hamiltonian import Hamiltonian
from scipy import sparse as sp

from TUM_quantum_sim.QW_sim.system import System


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
