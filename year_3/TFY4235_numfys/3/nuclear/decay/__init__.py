"""Module for nuclear decay calculations"""

from nuclear.decay.probability import decay

import numpy as np
from typing import Iterator

def run(Ns0: list[int], lambdas: list[float], dt: float, n: int) -> Iterator[list[int]]:
    """Run the decay algorithm for `n` timesteps. 

    Args:
        Ns0 (list[int]): List of initial particle amounts. Needs an extra element at the end to keep the leftovers
        lambdas (list[float]): probabilities of decaying
        dt (float): discrete timestep
        n(int): steps
    """
    Ns = Ns0
    for _ in range(n):
        for i, l in enumerate(lambdas):
            for _ in range(Ns[i]):
                if decay(dt, l):
                    Ns[i] -= 1
                    Ns[i+1] += 1 # this is fine as the Ns contain a dead-end failsafe as a last element
        yield Ns


def run_analytical(N0: int, lambdas: list[float], t: float) -> list[float]:
    """Calcualte the state at time `t`. Mutates the Ns

    Args:
        N0 (list[int]): Initial particle amount of particle 0
        lambdas (list[float]): probabilities of decaying
        t (float): Time at which to calculate the state
    
    Returns:
        list[float]: amounts of each atom. Can be non-integral
    """
    Ns = []
    lambdas = np.array(lambdas)

    for i in range(len(lambdas)):
        terms = []
        for k in range(i + 1):
            lambda_diff = lambdas[:i + 1] - lambdas[k]
            lambda_diff_prod = np.prod(lambda_diff, where=lambda_diff != 0)
            terms.append(np.exp(-lambdas[k] * t) / lambda_diff_prod)
        lambda_prod = np.prod(lambdas[:i])
        Ns.append(N0 * lambda_prod * sum(terms))

    Ns.append(N0 - sum(Ns))

    return Ns
        