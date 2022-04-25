"""Probabilities"""
# ^ tutorial on how to write good documentation right there

# can easily be swapped for std lib
from nuclear.utils import random
import numpy as np

def no_decay(dt: float, l: float) -> bool:
    """Sample the probability of not decaying, for a given delta t and lambda

    Args:
        dt (float): delta t
        l (float): lambda

    Returns:
        bool: true if no decay
    """
    return random() < np.exp(-l*dt)

def decay(dt: float, l: float) -> bool:
    """Sample the probability of decaying, for a given delta t and lambda

    Args:
        dt (float): delta t
        l (float): lambda

    Returns:
        bool: true if decay
    """
    return random() >= np.exp(-l*dt)
