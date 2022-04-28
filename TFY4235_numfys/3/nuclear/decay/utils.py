"""Small utility functions"""

import numpy as np

def half_life(l: float) -> float:
    """Calculate the half-life of an atom given its lambda

    Args:
        l (float): lambda

    Returns:
        float: half-life
    """
    return np.log(2) / l


def t_max(l: float, remainder: float) -> float:
    """Calculate the time at only `remainder` of the original amount remains

    Args:
        l (float): lambda
        remainder (float): float between 0 and 1

    Returns:
        float: time in seconds
    """
    return -np.log(remainder) / l

def steps(l: float, remainder: float, dt: float) -> int:
    """Calculate the steps necessary to have `remainder` left

    Args:
        l (float): lambda
        remainder (float): between 0 and 1
        dt (float): timestep

    Returns:
        int: steps
    """
    return int(t_max(l, remainder) / dt + 1)
