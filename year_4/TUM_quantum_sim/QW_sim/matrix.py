import numpy as np
from scipy import sparse as sp
import numba

from QW_sim.system import System
from QW_sim import physics
from QW_sim import constants

def hamiltonian(sys: System) -> np.ndarray:
    V = physics.potential(sys) * constants.e0

    dx = sys.Lx / sys.Nx
    dy = sys.Ly / sys.Ny

    f = constants.hbar**2 / (2 * constants.me * physics._effective_mass(0))
    cx = f / dx**2
    cy = f / dy**2
    c = cx + cy

    Dj = sp.diags([2*c, -cx, -cx], [0, 1, -1], shape=(sys.Nx, sys.Nx))

    H = sp.kron(sp.diags([1], shape=(sys.Ny, sys.Ny)), Dj)
    H += sp.diags([-cy, -cy], [sys.Nx, -sys.Nx], shape=(sys.Nx*sys.Ny, sys.Nx*sys.Ny))
    H += sp.diags(V.flatten())

    return H


def apply_boundary(sys: System, H: sp.spmatrix) -> sp.spmatrix:
    """Applies a zero-boundary condition

    Args:
        H (sp.spmatrix): hamiltonian

    Returns:
        sp.spmatrix: hamiltonian with boundary condition
    """

    # numba does not like objects. 
    # I did not bother testing with accessing directly
    nx = sys.Nx
    ny = sys.Ny

    # note: this is MUCH faster than alternatives if the boundary is more complex,
    # See `year_3\TFY4235_numfys\1\fractal_drum\int_version\eigensys.py`
    # For such a simple boundary, there are likely some better ways
    @numba.jit(nopython = True, parallel = True)
    def set_zeros(A_data, A_indptr):
        for i in numba.prange(ny):
            for j in range(nx):
                if i in [0, ny-1] or j in [0, nx-1]:
                    A_data[A_indptr[ny*j + i]:A_indptr[ny*j + i+1]] = 0

    set_zeros(H.data, H.indptr)
    H = H.tocsc()
    set_zeros(H.data, H.indptr)
    H.eliminate_zeros()

    # aight I'll just do this easier
    

    return H
