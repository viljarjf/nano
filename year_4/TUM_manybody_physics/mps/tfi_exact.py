"""Provides exact ground state energies for the transverse field ising model for comparison.

The Hamiltonian reads
.. math ::
    H = - J \\sum_{i} \\sigma^x_i \\sigma^x_{i+1} - g \\sum_{i} \\sigma^z_i
"""
import warnings
from functools import reduce

import numpy as np
import scipy.integrate
import scipy.sparse as sparse


def finite_gs_energy(L: int, J: float, g: float) -> float:
    """For comparison: obtain ground state energy from exact diagonalization.

    Exponentially expensive in L, only works for small enough `L` <~ 20.
    """
    if L >= 20:
        warnings.warn("Large L: Exact diagonalization might take a long time!")
    # get single site operaors
    sx = sparse.csr_matrix(np.array([[0.0, 1.0], [1.0, 0.0]]))
    sz = sparse.csr_matrix(np.array([[1.0, 0.0], [0.0, -1.0]]))
    id = sparse.csr_matrix(np.eye(2))
    sx_list = []  # sx_list[i] = kron([id, id, ..., id, sx, id, .... id])
    sz_list = []
    for i_site in range(L):
        x_ops = [id] * L
        z_ops = [id] * L
        x_ops[i_site] = sx
        z_ops[i_site] = sz
        X = reduce(lambda a, b: sparse.kron(a, b, "csr"), x_ops)
        Z = reduce(lambda a, b: sparse.kron(a, b, "csr"), z_ops)
        sx_list.append(X)
        sz_list.append(Z)
    H_xx = sparse.csr_matrix((2**L, 2**L))
    H_z = sparse.csr_matrix((2**L, 2**L))
    for i in range(L - 1):
        H_xx = H_xx + sx_list[i] * sx_list[(i + 1) % L]
    for i in range(L):
        H_z = H_z + sz_list[i]
    H = -J * H_xx - g * H_z
    E, V = scipy.sparse.linalg.eigsh(H, k=1, which="SA", return_eigenvectors=True)
    return E[0]


def infinite_gs_energy(J: float, g: float) -> float:
    """For comparison: Calculate groundstate energy density of an infinite system.

    The analytic formula stems from mapping the model to free fermions, see
    P. Pfeuty, The one-dimensional Ising model with a transverse field},
    Annals of Physics 57, p. 79 (1970).
    Note that we use Pauli matrices compared this reference using spin-1/2 matrices
    and replace the sum_k -> integral dk/2pi to obtain the result in the N-> infinity limit.
    """

    def f(k, lambda_):
        return np.sqrt(1 + lambda_**2 + 2 * lambda_ * np.cos(k))

    E0_exact = (
        -g
        / (J * 2.0 * np.pi)
        * scipy.integrate.quad(f, -np.pi, np.pi, args=(J / g,))[0]
    )
    return E0_exact
