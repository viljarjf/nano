import numpy as np
import numba

from scipy import sparse

from scipy.sparse._csc import csc_matrix

from . import properties, utils

@numba.njit
def generate_next_level(corners: np.ndarray) -> np.ndarray:
    """generate the next level of the fractal

    Args:
        corners (np.ndarray): 2 by n matrix of x/y coordinates of points

    Returns:
        np.ndarray: 2 by 8n matrix
    """
    n = corners.shape[1]
    out = np.zeros((2, 8*n), dtype = np.float32)

    x1 = corners[:, -1]

    for i in range(n):
        x2 = corners[:, i]

        x_vec = (x2 - x1)
        d = np.linalg.norm(x_vec) * 0.25            # length of new segment
        x_dir = d * x_vec / np.linalg.norm(x_vec)   # vector in x-direction
        y_dir = np.array([-x_dir[1], x_dir[0]])                    # vector in y-direction

        out[:, 8*i + 0] = x1
        out[:, 8*i + 1] = x1 + x_dir
        out[:, 8*i + 2] = x1 + x_dir + y_dir
        out[:, 8*i + 3] = x1 + 2*x_dir + y_dir
        out[:, 8*i + 4] = x1 + 2*x_dir
        out[:, 8*i + 5] = x1 + 2*x_dir - y_dir
        out[:, 8*i + 6] = x1 + 3*x_dir - y_dir
        out[:, 8*i + 7] = x1 + 3*x_dir

        x1 = x2
    
    return out

def reverse_iteration(x0: np.ndarray, x1: np.ndarray, x2: np.ndarray, l: int = 1) -> np.ndarray:
    """generate l iterations of point x0 with regards to line x1-x2, backwards

    Args:
        x0 (np.ndarray): point to transform
        x1 (np.ndarray): corner 1
        x2 (np.ndarray): corner 2
        l (int): iterations to perform

    Returns:
        np.ndarray: final position of point x0
    """

    def rot(p, c = np.zeros((2, 1)), cw = True):
        dir = p - c if cw else c - p
        return c + np.array([dir[1, :], -dir[0, :]])
    
    def flip(p, c):
        dir = p - c
        return c - dir
    
    def get_side(p, x1, x2):
        # -1 = left, 1 = right, 0 = on the line
        val = ((x2[0, :] - x1[0, :]) * (p[0, :] - x1[0, :]) - (x2[1, :] - x1[1, :]) * (p[1, :] - x1[1, :]))
        if abs(val) < 0.0001:
            return 0
        return 1 if val > 0 else -1

    vec = 0.25*(x2 - x1)
    ort = rot(vec, cw = False)
    diag = vec + ort
    ort_diag = vec - ort

    out = x0 - x1
    for _ in range(l):
        if get_side(out, 2*vec, 2*vec + diag) == 1:
            out = flip(out, 2*vec)
        s = get_side(out, vec + ort, vec + ort + ort_diag)
        if s == 1:
            out = rot(out, vec + ort)
        elif s == 0:
            if get_side(out, vec + 0.5*diag, vec + diag) == 1:
                out = rot(out, vec + ort)
        if get_side(out, vec, vec + ort_diag) >= 0:
            out = rot(out, vec, False)
        out *= 4

    return x1 + out


def generate_lattice(start: np.ndarray, l: int) -> np.ndarray:
    """Generate a lattice for a level l Koch snowflake, where start is the 0th level fractal

    Args:
        start (np.ndarray): the 4 starting corners of the fractal
        l (int): layer number, 0 for a square

    Returns:
        np.ndarray: 2 by n array
    """
    xmin = min(start[0, :])
    xmax = max(start[0, :])
    ymin = min(start[1, :])
    ymax = max(start[1, :])

    dx = (xmax - xmin)
    dy = (ymax - ymin)

    factor = (1 - 0.25**(l+1)) / 0.75 - 1
    x = np.arange(xmin - dy * factor, xmax + dy * factor + dx* 0.25**l, dx* 0.25**l, dtype = np.float32)
    y = np.arange(ymin - dx * factor, ymax + dx * factor + dy* 0.25**l, dy* 0.25**l, dtype = np.float32)

    return np.array(np.meshgrid(x, y))


def generate_sparce_matrix(lattice: np.ndarray, start: np.ndarray) -> csc_matrix:

    n = lattice.shape[1]
    center = sparse.diags([1, -4, 1], [-1, 0, 1], shape = (n, n), dtype = np.int8)
    not_center = sparse.diags([1], [0], shape = (n, n), dtype = np.int8)
    A = sparse.bmat(
        [[center, not_center] + [None]*(n-2)] + \
        [[None]*i + [not_center, center, not_center] + [None] * (n-3-i) for i in range(n-2)] + \
        [[None] * (n-2) + [not_center, center]], 
        dtype = np.float32, # necessary for eigenvalue calculations
        format = "csr"
    )

    @numba.jit(nopython = True, parallel = True)
    def set_zeros(A_data, A_indptr):
        for i in numba.prange(n):
            for j in numba.prange(n):
                if properties.is_inside(lattice[:, i, j], start) != 1:
                    utils.set_ind_to_0(A_data, A_indptr, n*j + i)

    set_zeros(A.data, A.indptr)
    A = A.tocsc()
    set_zeros(A.data, A.indptr)
    A.eliminate_zeros()
    A.sort_indices()
    return A
