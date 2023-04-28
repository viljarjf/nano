"""
Computational Methods in Many-Body Physics
Exercise 1, task 2:
Importance sampling with Monte Carlo
"""
import numpy as np
from matplotlib import pyplot as plt
import tqdm
from typing import Callable

def f(x: float) -> float:
    return np.exp(-x) / (x**2 - 2*x + 2)

alpha = 1.46
def g(x: float) -> float:
    return alpha * np.exp(-alpha * x)

def G(x: float) -> float:
    return 1 - np.exp(-alpha * x)

def G_inv(x: float) -> float:    
    return -np.log(1-x) / alpha

def I_uniform(N: int, a: float, b: float) -> float:
    x = np.random.uniform(a, b, N)
    I = f(x) * (b - a)
    return np.mean(I), np.var(I)


def I_sampled(N: int, a: float, b: float) -> float:
    x = G_inv(np.random.uniform(0, 1, N))
    I = f(x) / g(x)
    return np.mean(I), np.var(I)


def main():

    a = 0
    b = 10

    N = np.logspace(5, 14, 100, dtype=np.int32)
    print("UF: Uniform")
    print("IS: Importance sampling")
    for n in N:
        UF, UF_var = I_uniform(n, a, b)
        IS, IS_var = I_sampled(n, a, b)
        print(f"{n = }, {UF_var =  :.4e}, {IS_var =  :.4e}")
    

if __name__ == "__main__":
    main()
