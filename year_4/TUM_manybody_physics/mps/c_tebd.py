"""Toy code implementing the time evolving block decimation (TEBD)."""

import numpy as np
from scipy.linalg import expm

from . import tfi_exact
from .a_mps import MPS, split_truncate_theta
from .b_model import TFIModel

from typing import Iterator
from tqdm import tqdm


def calc_U_bonds(model: TFIModel, dt: float) -> list[np.ndarray]:
    """Given a model, calculate ``U_bonds[i] = expm(-dt*model.H_bonds[i])``.

    Each local operator has legs (i out, (i+1) out, i in, (i+1) in), in short ``i j i* j*``.
    Note that no imaginary 'i' is included, thus real `dt` means imaginary time evolution!
    """
    H_bonds = model.H_bonds
    d = H_bonds[0].shape[0]
    U_bonds = []
    for H in H_bonds:
        H = np.reshape(H, [d * d, d * d])
        U = expm(-dt * H)
        U_bonds.append(np.reshape(U, [d, d, d, d]))
    return U_bonds


def run_TEBD(
    psi: MPS, U_bonds: list[np.ndarray], N_steps: int, chi_max: int, eps: float
) -> None:
    """Evolve the state `psi` for `N_steps` time steps with (first order) TEBD.

    The state psi is modified in place."""
    [0 for _ in iterate_TEBD(psi, U_bonds, N_steps, chi_max, eps)]


def iterate_TEBD(
    psi: MPS, U_bonds: list[np.ndarray], N_steps: int, chi_max: int, eps: float
) -> Iterator[MPS]:
    """Evolve the state `psi` for `N_steps` time steps with (first order) TEBD.

    The state psi is modified in place."""
    Nbonds = psi.L - 1
    assert len(U_bonds) == Nbonds
    for n in tqdm(range(N_steps)):
        for k in [0, 1]:  # even, odd
            for i_bond in range(k, Nbonds, 2):
                update_bond(psi, i_bond, U_bonds[i_bond], chi_max, eps)
        yield psi
    # done

def iterate_TEBD_2nd_order(
    psi: MPS, U_bonds: list[np.ndarray], N_steps: int, chi_max: int, eps: float
) -> Iterator[MPS]:
    """Evolve the state `psi` for `N_steps` time steps with (second order) TEBD.

    The state psi is modified in place."""
    Nbonds = psi.L - 1
    assert len(U_bonds) == Nbonds
    for n in tqdm(range(N_steps)):
        for i_bond in range(0, Nbonds, 2):
            update_bond(psi, i_bond, U_bonds[i_bond]**0.5, chi_max, eps)
            update_bond(psi, i_bond, U_bonds[i_bond]**0.5, chi_max, eps)
        for i_bond in range(1, Nbonds, 2):
            update_bond(psi, i_bond, U_bonds[i_bond], chi_max, eps)
        yield psi
    # done

def update_bond(
    psi: MPS, i: int, U_bond: np.ndarray, chi_max: int, eps: float
) -> None:
    """Apply `U_bond` acting on i,j=(i+1) to `psi`."""
    j = i + 1
    # construct theta matrix
    theta = psi.get_theta2(i)  # vL i j vR
    # apply U
    Utheta = np.tensordot(
        U_bond, theta, axes=([2, 3], [1, 2])
    )  # i j [i*] [j*], vL [i] [j] vR
    Utheta = np.transpose(Utheta, [2, 0, 1, 3])  # vL i j vR
    # split and truncate
    Ai, Sj, Bj = split_truncate_theta(Utheta, chi_max, eps)
    # put back into MPS
    Gi = np.tensordot(
        np.diag(psi.Ss[i] ** (-1)), Ai, axes=[1, 0]
    )  # vL [vL*], [vL] i vC
    psi.Bs[i] = np.tensordot(Gi, np.diag(Sj), axes=[2, 0])  # vL i [vC], [vC] vC
    psi.Ss[j] = Sj  # vC
    psi.Bs[j] = Bj  # vC j vR


def example_TEBD_gs_finite(L: int, J: float, g: float) -> tuple[float, MPS, TFIModel]:
    print("finite TEBD, (imaginary time evolution)")
    print("L={L:d}, J={J:.1f}, g={g:.2f}".format(L=L, J=J, g=g))
    from . import a_mps, b_model

    model = b_model.TFIModel(L, J=J, g=g)
    psi = a_mps.init_spinup_MPS(L)
    for dt in [0.1, 0.01, 0.001, 1.0e-4, 1.0e-5]:
        U_bonds = calc_U_bonds(model, dt)
        run_TEBD(psi, U_bonds, N_steps=500, chi_max=30, eps=1.0e-10)
        E = model.energy(psi)
        print("dt = {dt:.5f}: E = {E:.13f}".format(dt=dt, E=E))
    print("final bond dimensions: ", psi.get_chi())
    if L < 20:  # for small systems compare to exact diagonalization
        E_exact = tfi_exact.finite_gs_energy(L, 1.0, g)
        print("Exact diagonalization: E = {E:.13f}".format(E=E_exact))
        print("relative error: ", abs((E - E_exact) / E_exact))
    return E, psi, model


if __name__ == "__main__":
    example_TEBD_gs_finite(L=14, J=1.0, g=1.5)
