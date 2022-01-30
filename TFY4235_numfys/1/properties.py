import numpy as np
import numba
from matplotlib import pyplot as plt


from . import utils

def distance_estimate(p: np.ndarray, start: np.ndarray, l: int, new) -> float:
    """check if a point p is inside or outside the fractal defined by a start and a level l

    Args:
        p (np.ndarray): [x, y]
        start (np.ndarray): starting points for the fractal
        l (int): depth of the fractal

    Returns:
        float: distance estimate
    """

    x1 = start[:, -1]
    d = float("inf")
    for i in range(start.shape[1]):
        x2 = start[:, i]
        current_p = p
        vec = (x2 - x1)
        ort_vec = utils.rotate(vec)
        for level in range(l):
            plt.plot(new[0, :], new[1, :])
            first_rotation_center = x1 + vec / 2
            current_p = 2*first_rotation_center - current_p
            plt.scatter(current_p[0], current_p[1], c = "r", marker = "x")
            plt.scatter(first_rotation_center[0], first_rotation_center[1], c = "r")

            second_rotation_center = x1 + vec / 4 + ort_vec / 4
            current_p = utils.rotate(current_p, second_rotation_center, -90)
            plt.scatter(current_p[0], current_p[1], c = "g", marker = "x")
            plt.scatter(second_rotation_center[0], second_rotation_center[1], c = "g")

            third_rotation_center = x1 + vec / 4
            current_p = utils.rotate(current_p, third_rotation_center, 90)
            plt.scatter(current_p[0], current_p[1], c = "b", marker = "x")
            plt.scatter(third_rotation_center[0], third_rotation_center[1], c = "b")

            current_p = x1 + 0.25*(current_p - x1)
            plt.scatter(current_p[0], current_p[1], c = "y")
            plt.show()
        d_new = 4**l*abs((x2[0] - x1[0])*(x1[1] - current_p[1]) - (x1[0] - current_p[0])*(x2[1] - x1[1]))/ np.linalg.norm(x2 - x1)
        d1 = np.linalg.norm(x1 - current_p)
        d2 = np.linalg.norm(x2 - current_p)
        d = min(d, max(d_new, d1), max(d_new, d2))
        x1 = x2
    
    return d