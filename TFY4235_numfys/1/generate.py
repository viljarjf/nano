import numpy as np
import numba

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

    xx, yy = np.meshgrid(x, y)

    return np.array([[xx.flatten()],[yy.flatten()]])