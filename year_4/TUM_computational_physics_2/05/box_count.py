import numpy as np
import numba

@numba.jit(nopython=True, parallel=True)
def rasterize(points: np.ndarray, shape: tuple[int, int]) -> np.ndarray:
    "(2, n) -> shape"
    out = np.zeros(shape, dtype=np.byte)
    Ny, Nx = shape
    for i in numba.prange(points.shape[1]):
        py, px = points[:, i]
        x = int(np.floor(px * Nx))
        y = int(np.floor(py * Ny))
        out[y, x] = 1
    return out

def box_fraction(points: np.ndarray, n_boxes: int) -> float:
    return np.count_nonzero(rasterize(points, (n_boxes, n_boxes))) / n_boxes**2
