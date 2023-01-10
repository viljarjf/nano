from scipy import sparse as sp
import numpy as np

from QW_sim.system import System

from dataclasses import dataclass

@dataclass
class Solution:
    eigenvalue: float | complex
    eigenvector: np.ndarray


def eigen(sys: System, H: sp.spmatrix, n: int = 5) -> list[Solution]:
    vals, vecs = sp.linalg.eigsh(H, k=n, which="SA")

    out = []
    for i in range(n):
        out.append(
            Solution(
                vals[i],
                vecs[:, i].reshape(sys.Ny, sys.Nx)
            )
        )
    return out
