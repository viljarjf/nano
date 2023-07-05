from functools import reduce

import numpy as np
from scipy import sparse as sp

# Copied from 05/lanczos.py
Id = sp.csr_matrix(np.eye(2), dtype=np.complex128)
Sx = sp.csr_matrix([[0.0, 1.0], [1.0, 0.0]], dtype=np.complex128)
Sz = sp.csr_matrix([[1.0, 0.0], [0.0, -1.0]], dtype=np.complex128)
Splus = sp.csr_matrix([[0.0, 1.0], [0.0, 0.0]], dtype=np.complex128)
Sminus = sp.csr_matrix([[0.0, 0.0], [1.0, 0.0]], dtype=np.complex128)


def _singlesite_to_full(op: sp.csr_matrix, i: int, L: int) -> sp.csr_matrix:
    assert i < L
    return reduce(
        lambda a, b: sp.kron(a, b, format="csr"),
        [op if n == i else Id for n in range(L)],
    )


def _gen_sx_list(L: int) -> list[sp.csr_matrix]:
    return [_singlesite_to_full(Sx, i, L) for i in range(L)]


def _gen_sz_list(L: int) -> list[sp.csr_matrix]:
    return [_singlesite_to_full(Sz, i, L) for i in range(L)]


def gen_hamiltonian(
    L: int, g: float, J: float = 1.0, periodic_boundary: bool = True
) -> sp.csr_matrix:
    """Generate a hamiltonian for the transverse field ising model

    :param L: System size
    :type L: int
    :param g: Field interaction strength
    :type g: float
    :param J: Spin neighbour interaction strength, defaults to 1.0
    :type J: float, optional
    :param periodic_boundary: If true, boundary is periodic. If false, boundary is open, defaults to True
    :type periodic_boundary: bool, optional
    :return: Full hamiltonian as a sparse matrix
    :rtype: sp.csr_matrix
    """
    sx_list = _gen_sx_list(L)
    sz_list = _gen_sz_list(L)
    H = sp.csr_matrix((2**L, 2**L), dtype=np.complex128)
    for j in range(L):
        H += -g * sz_list[j]
        # open boundary => skip neighbour interaction for first element
        if j or periodic_boundary:
            H += -J * (sx_list[j] * sx_list[(j - 1)])
    return H


def get_MPS_list(psi: np.ndarray, L: int, chi_max: int) -> list[np.ndarray]:
    """Generate a MPS representation of a state `psi`.
    Optionally compress the data with a chi smaller than 2**(L//2)

    :param psi: Ising model state, fulfilling psi.size == 2**L
    :type psi: np.ndarray
    :param L: System size
    :type L: int
    :param chi_max: Max dimension size for the internal matrices.
    If chi_max >= 2**(L//2), no compression is applied
    :type chi_max: int
    :return: List of matrices M_i, each with indices (alpha_i, j, alpha_i+1)
    :rtype: list[np.ndarray]
    """
    assert psi.size == 2**L
    assert chi_max > 0
    res = []
    psi_n = psi.reshape(1, -1)
    for n in range(L):
        chi_n, dim_R_n = psi_n.shape
        psi_n = psi_n.reshape(2 * chi_n, dim_R_n // 2)

        M_n, lambda_n, psi_n_tilde = np.linalg.svd(psi_n, full_matrices=False)

        if lambda_n.size > chi_max:
            # Stolen from the exercise sheet
            keep = np.argsort(lambda_n)[::-1][:chi_max]  # indices to keep
            M_n = M_n[:, keep]  # truncate matrix
            lambda_n = lambda_n[keep]  # truncate lambdas
            psi_n_tilde = psi_n_tilde[keep, :]  # truncate psi_tilde
        psi_n = lambda_n[:, np.newaxis] * psi_n_tilde[:, :]
        # End of stolen code

        chi_np1 = lambda_n.size

        res.append(M_n.reshape(chi_n, 2, chi_np1))
    return res


def get_MPS_tensor(psi: np.ndarray, L: int, chi_max: int) -> np.ndarray:
    """Full tensor MPS representation.
    Optionally compress the internal matrices with a chi smaller than 2**(L//2).
    Output has same shape regardless of compression

    :param psi: Ising model state, fulfilling psi.size == 2**L
    :type psi: np.ndarray
    :param L: System size
    :type L: int
    :param chi_max: Max dimension size for the internal matrices.
    If chi_max >= 2**(L//2), no compression is applied
    :type chi_max: int
    :return: Full MPS tensor, shape (1, *(2 for _ in range(L)), 1)
    :rtype: np.ndarray
    """
    return reduce(
        lambda a, b: np.tensordot(a, b, axes=(-1, 0)),
        get_MPS_list(psi, L, chi_max),
    )


def overlap(MPS_a: list[np.ndarray], MPS_b: list[np.ndarray]) -> float:
    """< MPS_b | MPS_a >, for two MPSs in list form

    :param MPS_a: MPS for ket state
    :type MPS_a: list[np.ndarray]
    :param MPS_b: MPS for bra state
    :type MPS_b: list[np.ndarray]
    :return: Overlap
    :rtype: float
    """
    assert len(MPS_a) == len(MPS_b)
    assert all(Ma.shape == Mb.shape for Ma, Mb in zip(MPS_a, MPS_b))

    # Sum over alpha_0 and j_0
    res = np.tensordot(MPS_a[0], MPS_b[0].conj(), axes=((0, 1), (0, 1)))

    for Ma, Mb in zip(MPS_a[1:], MPS_b[1:]):
        # Sum over j_i
        T = np.tensordot(Ma, Mb.conj(), axes=(1, 1))
        # Sum over alpha_j both above and below
        res = np.tensordot(res, T, axes=((0, 1), (0, 2)))
    return res.item().real
