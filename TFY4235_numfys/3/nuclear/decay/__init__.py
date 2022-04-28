"""Module for nuclear decay calculations"""

from nuclear.decay.probability import decay

import numpy as np
from typing import Generator

def run(Ns0: list[int], lambdas: list[float], dt: float, n: int) -> Generator[list[int], None, None]:
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


def run_analytical(N0: list[int], lambdas: list[float], t: float) -> list[float]:
    """Calcualte the state at time `t`. Mutates the Ns

    Args:
        N0 (list[int]): Initial particle amount of particle 0
        lambdas (list[float]): probabilities of decaying
        t (float): Time at which to calculate the state
    
    Returns:
        list[float]: amounts of each atom. Can be non-integral
    """
    Ns = [N0*np.exp(-lambdas[0]*t)]
    
    prod = lambda l: l[0]*prod(l[1:]) if l else 1
    diffsum = lambda l, lk: prod([li - lk for li in l])
    hk = lambda k: prod(lambdas[:k]) / diffsum(lambdas[:k], lambdas[k])

    for i in range(1, len(lambdas)):
        Ns.append(N0 * sum([hk(i)*np.exp(-lambdas[i]*t)]))

    Ns.append(N0 - sum(Ns))

    return Ns
        