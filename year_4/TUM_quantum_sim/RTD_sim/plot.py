"""

Plot stuff

"""

from matplotlib import pyplot as plt
import numpy as np

from RTD_sim.system import System

def potential(s: System, n: int = 200) -> None:
    plt.figure()
    z = np.linspace(0, s.L, n)
    V = np.vectorize(s.V)(z)
    plt.plot(z, V)
    plt.show()
