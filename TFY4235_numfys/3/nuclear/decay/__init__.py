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
