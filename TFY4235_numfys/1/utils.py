import numba
import numpy as np

def rotate(p, origin=(0, 0), degrees=90):
    angle = np.deg2rad(degrees)
    R = np.array([[np.cos(angle), -np.sin(angle)],
                  [np.sin(angle),  np.cos(angle)]])
    o = np.atleast_2d(origin)
    p = np.atleast_2d(p)
    return np.squeeze((R @ (p.T-o.T) + o.T).T)

@numba.njit
def is_inside_polygon(p: np.ndarray, poly: np.ndarray) -> int:
    """check if a point is inside or outside a polygon
        O(n)
    Args:
        p (np.ndarray): poitn
        poly (np.ndarray): 2 x n, polygon

    Returns:
        int: 1 if inside, -1 if outside, 0 if on polygon

    """ 
    # simple check: raycast along x-axis, count intersections. 
    # odd number: we are inside
    # even number: outside

    # this is a common problem, I'm just googling it
    # kok from https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/
    
    def onSegment(p, q, r):
        if p[0] > r[0]:
            x1, x2 = p[0], r[0]
        else:
            x1, x2 = r[0], p[0]
        if p[1] > r[1]:
            y1, y2 = p[1], r[1]
        else:
            y1, y2 = r[1], p[1]
        return (q[0] <= x1 and (q[0] >= x2)) and (q[1] <= y1 and (q[1] >= y2))
    
    def orientation(p, q, r):
        # to find the orientation of an ordered triplet (p,q,r)
        # function returns the following values:
        # 0 : Collinear points
        # 1 : Clockwise points
        # 2 : Counterclockwise
        
        # See https://www.geeksforgeeks.org/orientation-3-ordered-points/amp/
        # for details of below formula.
        
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if (val > 0):
            # Clockwise orientation
            return 1
        elif (val < 0):
            
            # Counterclockwise orientation
            return 2
        else:
            
            # Collinear orientation
            return 0
    
    # The main function that returns true if
    # the line segment 'p1q1' and 'p2q2' intersect.
    def doIntersect(p1,q1,p2,q2):
        
        # Find the 4 orientations required for
        # the general and special cases
        o1 = orientation(p1, q1, p2)
        o2 = orientation(p1, q1, q2)
        o3 = orientation(p2, q2, p1)
        o4 = orientation(p2, q2, q1)
    
        # Special Cases
    
        # p1 , q1 and p2 are collinear and p2 lies on segment p1q1
        if ((o1 == 0) and onSegment(p1, p2, q1)):
            return 1, False
    
        # p1 , q1 and q2 are collinear and q2 lies on segment p1q1
        if ((o2 == 0) and onSegment(p1, q2, q1)):
            return 1, False
    
        # p2 , q2 and p1 are collinear and p1 lies on segment p2q2
        if ((o3 == 0) and onSegment(p2, p1, q2)):
            return 0, True
    
        # p2 , q2 and q1 are collinear and q1 lies on segment p2q2
        if ((o4 == 0) and onSegment(p2, q1, q2)):
            return 0, True
    
        # General case
        if ((o1 != o2) and (o3 != o4)):
            return 2, False

        # If none of the cases
        return 0, False

    n = 0
    p0 = poly[:, -1]
    p_inf = p0 + np.array([11, -2])
    for i in range(poly.shape[1]):
        p1 = poly[:, i]
        inter, on_border = doIntersect(p, p_inf, p0, p1)
        if on_border:
            return 0
        n += inter
        p0 = p1
    n //= 2
    return 1 if n%2 else -1

#@numba.njit
def is_inside_convex_quadrilateral(p: np.ndarray, poly: np.ndarray) -> int:
    """better restriction on the polygon = better is_inside function

    Args:
        p (np.ndarray): point
        poly (np.ndarray): corners of convex quadrilateral, in clockwise order

    Returns:
        bool: big if true
    """
    e = 0.001
    def orientation(l0, l1, point):        
        return ((l1[0] - l0[0])*(point[1] - l0[1]) - (l1[1] - l0[1])*(point[0] - l0[0]))

    res = True
    intersect = False
    p0 = poly[:, -1]
    for i in range(poly.shape[1]):
        p1 = poly[:, i]
        v = orientation(p0, p1, p)
        if abs(v) < e:
            intersect = True
        res &= (v < e)
        p0 = p1
    if intersect and res:
        return 0
    return 1 if res else -1
