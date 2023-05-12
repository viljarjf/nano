
from .square_lattice import IsingModel
import numpy as np
from numba import njit, prange

class TriangularIsingModel(IsingModel):

    # We only need to update the lookup table for the bonds.
    # The triangular lattice has 6 bonds per lattice cite.
    # To index them, we consider a regular square lattice as before,
    # but we squeeze it to a rhombus.
    @staticmethod
    @njit(parallel=True)
    def __jit_get_init_bond_indices(shape: tuple[int]) -> np.ndarray:
        Ly, Lx = shape
        N = Lx * Ly

        def xy_2_idx(x: int, y: int) -> int:
            return Ly * x + y
    
        def idx_2_xy(idx: int) -> tuple[int, int]:
            return divmod(idx, Ly)  
        
        bond_indices = np.empty((3*N, 2), dtype=np.int32)
        for n in prange(N):
            x, y = idx_2_xy(n)
            # -
            bond_indices[2*n, 0] = n
            bond_indices[2*n, 1] = xy_2_idx(x, (y + 1) % Ly)
            # /
            bond_indices[2*n + 1, 0] = n
            bond_indices[2*n + 1, 1] = xy_2_idx((x + 1) % Lx, y)
            # \
            bond_indices[2*n + 1, 0] = n
            bond_indices[2*n + 1, 1] = xy_2_idx((x + 1) % Lx, (y + 1) % Ly)
        return bond_indices
    