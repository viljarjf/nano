"""Set up and solve the eigensystem"""

import numpy as np
from scipy import sparse
import numba

from fractal_drum.int_version import lattice

def matrix_without_boundary(n: int) -> sparse.csr_matrix:
    inner = sparse.diags([1, -4, 1], [-1, 0, 1], shape = (n, n), dtype = np.int8)
    outer = sparse.diags([1], [0], shape = (n, n), dtype = np.int8)
    inner_spots = sparse.identity(n, dtype=np.int8)
    outer_spots = sparse.diags(
        [1, 0, 1], 
        [-1, 0, 1], 
        shape=(n, n), 
        dtype=np.int8, 
    )
    A = sparse.kron(inner, inner_spots) + \
        sparse.kron(outer, outer_spots)
    return A.astype(np.float32)

def big_matrix_without_boundary(n: int) -> sparse.csr_matrix:
    inner = sparse.diags([-1, 16, -60, 16, -1], [-2, -1, 0, 1, 2], shape = (n, n), dtype = np.int8)
    middle = 16 * sparse.identity(n, dtype = np.int8)
    outer = -sparse.identity(n, dtype=np.int8)

    inner_spots = sparse.identity(n, dtype=np.int8)
    middle_spots = sparse.diags(
        [1, 0, 1], 
        [-1, 0, 1], 
        shape=(n, n), 
        dtype=np.int8, 
    )
    outer_spots = sparse.diags(
        [1, 0, 1], 
        [-2, 0, 2], 
        shape=(n, n), 
        dtype=np.int8, 
    )
    A = sparse.kron(inner, inner_spots) + \
        sparse.kron(middle, middle_spots) + \
        sparse.kron(outer, outer_spots)
    return A.astype(np.float32)


def apply_boundary(eigsys: sparse.csr_matrix, fractal: np.ndarray) -> tuple[sparse.csc_matrix, np.ndarray]:
    n = fractal.shape[0]

    @numba.jit(nopython = True, parallel = True)
    def set_zeros(A_data, A_indptr):
        for i in numba.prange(n):
            for j in numba.prange(n):
                if fractal[i, j] != lattice.IN:
                    A_data[A_indptr[n*j + i]:A_indptr[n*j + i+1]] = 0

    set_zeros(eigsys.data, eigsys.indptr)
    eigsys = eigsys.tocsc()
    set_zeros(eigsys.data, eigsys.indptr)
    eigsys.eliminate_zeros()

    # remove zero-rows
    indices = eigsys.getnnz(0)>0
    eigsys = eigsys[eigsys.getnnz(1)>0][:,eigsys.getnnz(0)>0]
    
    return eigsys, indices


def fill_eigenvector(l: int, sub: int, eigenvec: np.ndarray, indices) -> np.ndarray:
    n2 = lattice.calc_n(l, sub)**2
    out = np.zeros(n2, dtype=eigenvec.dtype)
    out[indices] = eigenvec
    return out
