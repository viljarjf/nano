from re import L
import numpy as np

def rotate(p, origin=(0, 0), degrees=90):
    angle = np.deg2rad(degrees)
    R = np.array([[np.cos(angle), -np.sin(angle)],
                  [np.sin(angle),  np.cos(angle)]])
    o = np.atleast_2d(origin)
    p = np.atleast_2d(p)
    return np.squeeze((R @ (p.T-o.T) + o.T).T)


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

    class LocalError(Exception):
        pass
    
    def onSegment(p, q, r):
        if ( (q[0] <= max(p[0], r[0])) and (q[0] >= min(p[0], r[0])) and
            (q[1] <= max(p[1], r[1])) and (q[1] >= min(p[1], r[1]))):
            return True
        return False
    
    def orientation(p, q, r):
        # to find the orientation of an ordered triplet (p,q,r)
        # function returns the following values:
        # 0 : Collinear points
        # 1 : Clockwise points
        # 2 : Counterclockwise
        
        # See https://www.geeksforgeeks.org/orientation-3-ordered-points/amp/
        # for details of below formula.
        
        val = (float(q[1] - p[1]) * (r[0] - q[0])) - (float(q[0] - p[0]) * (r[1] - q[1]))
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
            return 1
    
        # p1 , q1 and q2 are collinear and q2 lies on segment p1q1
        if ((o2 == 0) and onSegment(p1, q2, q1)):
            return 1
    
        # p2 , q2 and p1 are collinear and p1 lies on segment p2q2
        if ((o3 == 0) and onSegment(p2, p1, q2)):
            raise LocalError
    
        # p2 , q2 and q1 are collinear and q1 lies on segment p2q2
        if ((o4 == 0) and onSegment(p2, q1, q2)):
            raise LocalError
    
        # General case
        if ((o1 != o2) and (o3 != o4)):
            return 2

        # If none of the cases
        return 0

    n = 0
    p0 = poly[:, -1]
    p_inf = p + np.array([max(poly[0,:]) + 1, 1])
    try:
        for i in range(poly.shape[1]):
            p1 = poly[:, i]
            n += doIntersect(p, p_inf, p0, p1)
            p0 = p1
    except LocalError:
        return 0
    n //= 2
    return 1 if n%2 else -1