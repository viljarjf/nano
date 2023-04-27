"""
Exercise 1, Computational Methods in Many-Body Physics
"""
import numpy as np
from matplotlib import pyplot as plt
import tqdm

# Task 1.1 a
#   Estimate π by “shooting” (i.e., drawing random numbers) N times uniformly on a
#   square and counting the number of points hitting a disc target: the ratio of hits to
#   N should correspond to the ratio of the areas of the target to the area you shoot
#   on.

def mc_hypersphere_volume(N: int, d: int) -> float:
    """Calculate the volume of a `d`-dimensional hypersphere 
    with radius of 1, with Monte Carlo simulation

    Args:
        N (int): Simulation runs. Each run generates `d` random numbers
        d (int): Dimension of the hypersphere

    Returns:
        float: Estimate for hypersphere volume
    """
    random_numbers = np.random.uniform(-1, 1, (N, d))
    inside_circle = np.sum(random_numbers**2, axis=1) < 1
    return 2**d * np.count_nonzero(inside_circle) / N


def mc_calc_pi(N: int) -> float:
    """Calculate pi with Monte Carlo simulation

    Args:
        N (int): Simulation runs. Each run generates 2 random numbers

    Returns:
        float: Estimate for pi
    """
    return mc_hypersphere_volume(N, 2)


def mc_calc_pi_vectorized(N: int, M: int) -> np.ndarray:
    """Calculate pi with Monte-Carlo simulation, with N random samples, M times

    Args:
        N (int): Monte-Carlo iterations. 2 random samples per iteration
        M (int): Amount of times to perform the simulation

    Returns:
        np.ndarray: shape (M,), pi estimates
    """
    return np.vectorize(mc_calc_pi)([N]*M)


def mc_pi_variance(N: int, M: int) -> float:
    """Calculate the variance of Monte-Carlo estimate for pi

    Args:
        N (int): MC iterations per simulation
        M (int): Simulations to take the variance over

    Returns:
        float: Total variance
    """
    pi_arr = mc_calc_pi_vectorized(N, M)
    return np.var(pi_arr - np.pi)


def task_1():
    N = 1000
    print(f"Pi = {mc_calc_pi(N)} ({N = })")

    N = [i for i in range(10, 1000, 5)]
    M = 1000
    pi_var = []
    for n in tqdm.tqdm(N):
        pi_var.append(mc_pi_variance(n, M))
    
    plt.figure()
    plt.plot(N, pi_var)
    plt.plot(
        [N[0], N[-1]],
        [pi_var[0], pi_var[-1]]
        )
    plt.legend([
        "Variance",
        f"Slope: {np.log((pi_var[-1]) - np.log(pi_var[0])) / (np.log(N[-1]) - np.log(N[0])) :.2e}"
    ])
    plt.xlabel("N")
    plt.ylabel("Variance")
    plt.xscale("log")
    plt.yscale("log")
    plt.title("Monte-Carlo estimation of $\\pi$, Variance of error")
    plt.show()

    


def main():
    task_1()

if __name__ == "__main__":
    main()