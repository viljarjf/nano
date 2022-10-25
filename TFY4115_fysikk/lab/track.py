"""

Interpolate pre-determined points to a track

"""

from math import atan

from typing import Callable
from scipy.interpolate import CubicSpline
from scipy.optimize import minimize

from lab.dataclasses import Point

_TRACK_DELTA_X  = 0.2   # [m]
_TRACK_X0       = 0.0   # [m]

class Track(CubicSpline):
    
    def __init__(self, y_pos: list[float]):
        x_pos = [_TRACK_X0 + _TRACK_DELTA_X * i for i in range(len(y_pos))]
        super().__init__(x_pos, y_pos, bc_type="natural")

    def _distance_function(self, point: Point) -> Callable[[float], float]:
        """Returns a function of x, 
        where the output is the distance from the track at x to the given point

        Example:

        t = Track([0,0]) # flat track
        p = Point(0,0)
        f = t._distance_function(point)
        
        f(0)
        >>> 0.0

        f(1)
        >>> 1.0

        Args:
            point (Point): point used for distance calculation in the returned function

        Returns:
            Callable[[float], float]: function of x (float) returning distance (float)
        """
        x0, y0 = point.x, point.y
        return lambda x: ((x - x0)**2 + (self(x) - y0)**2)**0.5


    def closest_point(self, point: Point) -> float:
        """Find the point on the track closest to the given point

        Args:
            point (Point): (x, y) point

        Returns:
            float: x-value of the closest point on track
        """
        dist_func = self._distance_function(point)
        min_result = minimize(dist_func, point.x)
        return min_result.x[0]


    def distance(self, point: Point) -> float:
        """Calculate the distance from a point (x, y) to the track

        Args:
            point (Point): (x, y) position to calculate the distance to

        Returns:
            float: distance from point to track
        """
        dist_func = self._distance_function(point)
        min_x = self.closest_point(point)
        return dist_func(min_x)


    def inverse_curvature(self, x: float) -> float:
        """Calculate the (signed) inverse curvature of the track at a point x

        1 / R = y'' / (1 + y'^2)^3/2

        Args:
            x (float): x-value to calculate curvature for

        Returns:
            float: curvature, signed
        """
        return self.derivative(2)(x) / (1 + self.derivative()(x)**2)**1.5
    
    def angle(self, x: float) -> float:
        """Calculate the angle between the track and the horizontal at a point x

        Args:
            x (float): point along the track

        Returns:
            float: angle
        """
        return atan(-self.derivative()(x))
