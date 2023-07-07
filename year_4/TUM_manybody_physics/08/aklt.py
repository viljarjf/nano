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
    """Generate a MPS representation of a spin-1/2 state `psi`.
    Optionally compress the data with a chi smaller than 2**(L//2)

    :param psi: Spin-1/2 state, fulfilling psi.size == 2**L
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
    """Full tensor MPS representation for a spin-1/2 sate.
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
    return MPS_list_to_tensor(get_MPS_list(psi, L, chi_max))


def MPS_list_to_tensor(MPS: list[np.ndarray]) -> np.ndarray:
    """Convert a MPS list format to MPS tensor format

    :param MPS: MPS list format
    :type MPS: list[np.ndarray]
    :return: MPS tensor format
    :rtype: np.ndarray
    """
    return reduce(
        lambda a, b: np.tensordot(a, b, axes=(-1, 0)),
        MPS,
    )


def overlap(bra: list[np.ndarray], ket: list[np.ndarray]) -> float:
    """< bra | ket >, for two MPSs in list form

    :param bra: MPS for bra state
    :type bra: list[np.ndarray]
    :param ket: MPS for ket state
    :type ket: list[np.ndarray]
    :return: Overlap
    :rtype: float
    """
    assert len(bra) == len(ket)

    res = np.eye(1)

    for bra_i, ket_i in zip(bra, ket):
        # Sum over alpha_i
        res = np.tensordot(res, ket_i, axes=(1, 0))
        # Sum over alpha_j and j_i
        res = np.tensordot(bra_i.conj(), res, axes=((0, 1), (0, 1)))
    return np.linalg.norm(res.item())


def get_minimum_chi(psi: np.ndarray, L: int, chi_0: int = 20) -> None:
    """Iterate through smaller and smaller chi
    untill the compressed state is sufficiently different to the original state

    :param psi: State
    :type psi: np.ndarray
    :param L: System size
    :type L: int
    :param chi_0: Initial chi, defaults to 20
    :type chi_0: int, optional
    """

    # Man, do while would be nice right now
    M = get_MPS_tensor(psi, L, 2 ** (L // 2))
    chi = chi_0
    while np.allclose(M.ravel(), psi.ravel()) and chi > 1:
        chi -= 1
        M = get_MPS_tensor(psi, L, chi)

    if chi == chi_0:
        print(
            "MPS representation did not correspond to original representation "
            f"with {chi_0 = }."
        )
        return -1

    return chi + 1  # Once again, do while would be nice


def deepcopy_MPS(MPS: list[np.ndarray]) -> np.ndarray:
    """Deep copy a MPS"""
    return [np.copy(M) for M in MPS]


def apply_op_at_site(
    MPS: list[np.ndarray], op: np.ndarray, i: int) -> list[np.ndarray]:
    """Applies the local operator `op` at site `i`

    :param MPS: State
    :type MPS: list[np.ndarray]
    :param op: 2x2 matrix operator
    :type op: np.ndarray
    :param i: Index to apply operator
    :type i: int
    :return: State
    :rtype: list[np.ndarray]
    """
    out = MPS.copy()
    out[i] = np.tensordot(out[i], op, axes=(1, 0)).reshape(out[i].shape)
    return out


def operator_correlation(MPS: list[np.ndarray], op: np.ndarray) -> np.ndarray:
    """Calculate the spatial correlation of a local operator

    :param MPS: State
    :type MPS: list[np.ndarray]
    :param op: Operator
    :type op: np.ndarray
    :return: LxL matrix, such that mat[i, j] = <op_i op_j>
    :rtype: np.ndarray
    """
    L = len(MPS)
    out = np.empty((L, L), dtype=np.complex128)
    for i in range(L):
        for j in range(L):
            MPS_i = apply_op_at_site(MPS, op, i)
            MPS_j = apply_op_at_site(MPS, op, j)

            op_i = overlap(MPS_i, MPS)
            op_j = overlap(MPS_j, MPS)

            MPS_ij = apply_op_at_site(MPS_i, op, j)

            op_ij = overlap(MPS_ij, MPS)

            out[i, j] = op_ij - op_i * op_j
    return out
