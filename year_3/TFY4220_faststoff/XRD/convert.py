"""Do some math"""
from math import sin, radians

LAMBDA = 0.7093 # Å

def two_theta_to_d(twotheta: float) -> float:
    """calculate d from 2theta.
    output in Å
    """
    return LAMBDA / (2 * sin(radians(twotheta / 2)))
