"""
Computational Methods for Nanoelectronics: Quantum Models
Exercise 1

I should really start using jupyter notebooks for stuff like this
"""

import numpy as np
from matplotlib import pyplot as plt

def Psi(x: float, x_0: float, sigma_0: float, k_0: float) -> complex | np.ndarray:
    a = (sigma_0 / (2*np.pi)**0.5)**0.5
    b = (x - x_0)**2 / (4 * sigma_0**2)
    c = 1j * k_0 * (x - x_0)
    return a * np.exp(-b + c)

def Psi_t(x: float, t: float, x_0: float, sigma_0: float, k_0: float) -> complex:
    a = (sigma_0 / (2*np.pi)**0.5)**0.5
    b = (sigma_0**2 + 0.5j*t)**-0.5
    c = np.exp(-sigma_0**2 * k_0**2)
    d = (x - x_0 - 2j * sigma_0**2 * k_0)**2
    e = 4 * (sigma_0**2 + 0.5j*t)
    f = np.exp(-d / e)
    return a*b*c*f

def rho(x: float, t: float, x_0: float, sigma_0: float, k_0: float) -> float | np.ndarray:
    sigma = sigma_0 * (1 + (t**2) / (4 * sigma_0**4))**0.5
    a = 1 / (sigma * (2*np.pi)**0.5)
    b = (x - x_0 - k_0 * t)**2
    return a * np.exp(-b / (2*sigma**2))

def dxdk(t: float, sigma_0: float) -> float:
    dx = sigma_0 * (1 + (t**2) / (4 * sigma_0**4))**0.5
    dk = 1 / (2*sigma_0)
    return dx*dk


def task_1():
    L = 10
    N = 300
    x = np.linspace(0, L, N)
    t = 0
    x_0 = L / 2
    k_0 = 5 * np.pi
    sigma_0 = L / 20

    psi = Psi(x, x_0, sigma_0, k_0)
    
    plt.figure()
    plt.suptitle("$\\Psi$")
    plt.subplot(1, 2, 1)
    plt.plot(psi.real)
    plt.title("$\\Re$")
    plt.subplot(1, 2, 2)
    plt.plot(psi.imag)
    plt.title("$\\Im$")
    plt.show()


def task_2():
    L = 10
    N = 300
    x = np.linspace(0, L, N)
    t = 0
    x_0 = L / 2
    k_0 = 0 * np.pi
    sigma_0 = L / 20

    t0 = 0
    t1 = 1

    def plot(k_0):
        plt.figure()
        plt.suptitle(f"$\\rho, {k_0 = }$")
        plt.subplot(1, 2, 1)
        plt.plot(rho(x, t0, x_0, sigma_0, k_0))
        plt.title(f"t = {t0}")
        plt.subplot(1, 2, 2)
        plt.plot(rho(x, t1, x_0, sigma_0, k_0))
        plt.title(f"t = {t1}")
        plt.show()

    plot(k_0=0)
    plot(k_0=np.pi)

def task_3():
    pass

def main():
    task_1()
    task_2()
    task_3()


if __name__ == "__main__":
    main()
