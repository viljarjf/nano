"""Heun numerical scheme"""

import numpy as np
from typing import Callable


def step(
    dt: float, 
    Sj: np.ndarray, 
    dSj: Callable[[np.ndarray], np.ndarray]
    ) -> np.ndarray:

    dSjp = dSj(Sj)
    Sj1p = normalize(Sj + dt*dSjp)

    Sj1 = normalize(Sj + dt/2*(dSjp + dSj(Sj1p)))
    
    return Sj1


def normalize(Sj: np.ndarray) -> np.ndarray:
    l = np.linalg.norm(Sj, axis=-1, keepdims=True)
    l[l == 0] = 1
    return Sj / l
