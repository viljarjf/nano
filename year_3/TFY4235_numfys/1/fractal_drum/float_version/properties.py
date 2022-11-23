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
    # its just a reverse transformation at this point... not really a working distance estimator
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

@numba.njit
def is_inside(point: np.ndarray, start: np.ndarray) -> int:
    """returns whether a point is inside or outside the curve

    Args:
        p (np.ndarray): x/y point
        start (np.ndarray): the four starting points, given in a clockwise manner

    Returns:
        int: 1 if inside, -1 if outside, 0 if on border
    """
    # transform to an easy-to-work-with basis
    p0 = start[:, 0]

    # epsilon: small number to negate floating point precision
    e = 0.00001

    p = point - p0
    a = np.linalg.norm(p0 - start[:, 1])
    b = np.linalg.norm(start[:, -1] - p0)
    ct = (start[:, -1] - p0)[1] / b
    st = np.math.sin(np.math.acos(ct))
    p = np.array([
        a*ct*p[0] + a*st*p[1], 
       -b*st*p[0] + b*ct*p[1]
        ])
    
    # now we need to check if the point p is inside or outside the standard 1x1 fractal

    # first, check the largest bounding box
    bounding_box = np.array([[0, -1, 0, 1, 3, 4, 3, 2], [0, 1, 3, 4, 3, 2, 0, -1]])
    small_bounding_box = np.array([[0, 1, 3, 2], [0, 1, 0, -1]])
    smaller_bounding_boxes = np.array([
        [
            [0, 1, 3, 2], 
            [0, 1, 0, -1]
        ],[
            [3, 2, 3, 4], 
            [0, 1, 3, 2]
        ], [
            [3, 4, 6, 5], 
            [3, 4, 3, 2]
        ],[
            [6, 7, 6, 5], 
            [3, 2, 0, 1]
        ], [
            [6, 7, 6, 5], 
            [0, -1, -3, -2]
        ]
    ])
    final_polygon = np.array([
        [1, 3, 3],
        [1, 0, 3]
    ])
    if utils.is_inside_convex_quadrilateral(3*p, bounding_box) >= 0:
        # inside the box, need more processing

        # if it is on a diagonal, it is guaranteed to be inside 
            # this also ensures that we don't need to consider edge cases of points being on a diagonal
        #if p[1] == p[0] or p[1] == 1-p[0]:
        #    return 1

        # we know everything is rotationally symmetric around (0.5, 0.5), so we can just tansform the point down
        
        # above y=x, we rotate 180
        if  (p[1] > p[0] + e and p[1] <= 0.5) or \
            (p[1] > p[0] - e and p[1] >= 0.5):
            p = 1-p
        
        # above y=1-x, rotate 90 deg cockwise
        if p[1] >= 1-p[0]:
            p[0], p[1] = p[1], 1 - p[0]
        
        # if now outside the small bounding box, it is inside the big bounding box
        if utils.is_inside_convex_quadrilateral(3*p, small_bounding_box) == -1:
            return 1
        
        # if we reach this point, we need to loop down on the single fractal
        # to see if any of the 8 smaller bounding boxes contain the point
        flip_side = 1
        while True:
            # to reduce our work, we flip everything to the right of the middle
            # remember to also flip whether we are outside or inside
            if p[0] > 0.5:
                p = np.array([1, 0])-p
                flip_side *= -1

            # check if we are on the curve
            if abs(p[1]) < e and (abs(p[0]) < e or abs(p[0] - 1) < e):
                return 0
            
            # check the 5 smaller bounding boxes
            # also, multiply by 12 to work with integers for the bounding box
            p *= 12
            break_loop = False
            for i in range(smaller_bounding_boxes.shape[0]):
                if utils.is_inside_convex_quadrilateral(p, smaller_bounding_boxes[i, :, :]) >= 0:
                    # we are inside (or on the edge of) a smaller box! Transform a little and try again
                    p0 = smaller_bounding_boxes[i, :, 0]
                    p1 = smaller_bounding_boxes[i, :, 2] - p0
                    p -= p0
                    if p1[1] > 0:
                        p[0], p[1] = p[1], -p[0]

                    elif p1[1] < 0:
                        p[0], p[1] = -p[1], p[0]

                    p /= 3 # 12/3 = 4 in total
                    
                    break_loop = True
                    break
            if break_loop:
                continue
            
            # Great! Now we only need to check three polygons to determine if we are in or out
            is_in_bounding_box = utils.is_inside_polygon(p, final_polygon)
            if is_in_bounding_box < 0:
                # not inside this polygon => outside
                return -flip_side
            # we are inside even if we are on the edge of this polygon
            return flip_side
    else:
        return -1


def set_zero(i, j, n, arr):
    n = int(arr.shape[0]**0.5)
    indices = [(n*j + i + 0, n*j + i + 0)]
    if i < n-1:
        indices += [
        (n*j + i + 1, n*j + i + 0),
        (n*j + i + 0, n*j + i + 1)
        ]
    if i > 0:
        indices += [
        (n*j + i - 1, n*j + i + 0),
        (n*j + i + 0, n*j + i - 1)
        ]
    if j < n-1:
        indices += [
        ((j + 1)*n + i, (j - 0)*n + i),
        ((j - 0)*n + i, (j + 1)*n + i)
        ]
    if j > 0:
        indices += [
        ((j - 1)*n + i, (j - 0)*n + i),
        ((j - 0)*n + i, (j - 1)*n + i)
        ]
        
    for y, x in indices:
        arr[y, x] = 0

