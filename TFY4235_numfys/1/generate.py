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
