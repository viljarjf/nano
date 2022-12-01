"""

Plot stuff

"""

from matplotlib import pyplot as plt
import numpy as np

from RTD_sim.system import System
from RTD_sim import constants as c
from RTD_sim.transfer_matrix import Td

def potential(s: System, N: int = 200) -> None:
    plt.figure()
    z = np.linspace(0, s.L, N)
    V = np.vectorize(s.V)(z)
    plt.plot(z / 1e-9, V / c.e0)
    plt.xlabel("z [nm]")
    plt.ylabel("V [eV]")
    plt.show()

def probability_density(E: float, s: System, N: int) -> None:
    E *= c.e0
    psi1 = lambda x: np.exp(1j*s.k(E, x)*x) 
    psi2 = lambda x: np.exp(-1j*s.k(E, x)*x)

    p1 = np.zeros(N, dtype=np.complex128)
    p2 = np.zeros(N, dtype=np.complex128)
    z = np.linspace(0, s.L, N)
    dz = z[1] - z[0]

    coefs = np.array([[1],[0]])

    for n in range(N):
        p1[n] = coefs[0]*psi1(z[n])
        p2[n] = coefs[1]*psi2(z[n])
        if n+1 == N:
            break
        k1 = s.k(E, z[n])
        k2 = s.k(E, z[n+1])
        T = Td(k1, k2, z[n])
        coefs = np.matmul(T, coefs)
    
    f = z < 2.0e-9
    plt.figure()
    plt.plot(z[f], np.real(p1)[f])
    plt.show()

    plt.figure()
    plt.plot(z[f], (abs(p1)**2)[f])
    plt.show()
