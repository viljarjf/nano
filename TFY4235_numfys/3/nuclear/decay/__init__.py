"""Module for nuclear decay calculations"""

from nuclear.decay.probability import decay

import numpy as np

def run(Ns: list[int], lambdas: list[float], dt: float) -> None:
    """Run the decay algorithm for a single timestep. Mutates the Ns

    Args:
        Ns (list[int]): List of particle amounts. Needs an extra element at the end to keep the leftovers
        lambdas (list[float]): probabilities of decaying
        dt (float): discrete timestep
    """
    for i, l in enumerate(lambdas):
        for _ in range(Ns[i]):
            if decay(dt, l):
                Ns[i] -= 1
                Ns[i+1] += 1 # this is fine as the Ns contain a dead-end failsafe as a last element
    return Ns


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

def n(l: float, remainder: float, dt: float) -> int:
    """Calculate the steps necessary to have `remainder` left

    Args:
        l (float): lambda
        remainder (float): between 0 and 1
        dt (float): timestep

    Returns:
        int: steps
    """
    return int(t_max(l, remainder) / dt + 1)