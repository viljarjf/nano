import numpy as np
import numba
from abc import ABC, abstractmethod


class Metropolis(ABC):
    spins: np.ndarray
    SPIN_UP = 1
    SPIN_DOWN = -1

    def __init__(self, N: int | tuple[int, int], J: float, g: float):
        self.N = N
        self.ndim = len(tuple(N))
        self.J = J
        self.g = g
        self.init_random()

    def init_random(self):
        self.spins = np.random.randint(0, 3, self.N, dtype=np.int8) - 1

    def init_up(self):
        self.spins = np.ones(self.N, dtype=np.int8)

    def init_down(self):
        self.spins = -np.ones(self.N, dtype=np.int8)

    @abstractmethod
    def get_neighbours(self, n: int | tuple[int, int]) -> list[int | tuple[int, int]]:
        pass

    @abstractmethod
    def get_random_site(self) -> int | tuple[int, int]:
        pass

    def energy_at_site(self, n: int | tuple[int, int]) -> float:
        """calculate the energy of site `n`

        :param n: Site to check
        :type n: int | tuple[int, int]
        :return: E
        :rtype: float
        """
        neighbours = self.get_neighbours(n)
        return (-self.J * np.sum(self.spins[neighbours]) - self.g) * self.spins[n]

    def energy_difference(self, n: int | tuple[int, int]) -> float:
        """calculate the energy difference if site `n` were to be flipped

        :param n: Site to check
        :type n: int | tuple[int, int]
        :return: E
        :rtype: float
        """
        return 2 * self.energy_at_site(n)

    def perform_iter(self, kbT: float):
        site = self.get_random_site()
        dE = self.energy_difference(site)
        if np.random.random() < np.exp(-dE / kbT):
            self.spins[site] = -self.spins[site]


class Metropolis1D(Metropolis):
    def get_neighbours(self, n: int) -> list[int]:
        return [(n - 1) % self.N, (n + 1) % self.N]

    def get_random_site(self) -> int:
        return np.random.randint(0, self.N)


class Metropolis2D(Metropolis):
    def get_neighbours(self, n: tuple[int, int]) -> list[tuple[int, int]]:
        x, y = n
        Nx, Ny = self.N
        return [
            ((x + 1) % Nx, y),
            ((x - 1) % Nx, y),
            (x, (y + 1) % Ny),
            (x, (y - 1) % Ny),
        ]

    def get_random_site(self) -> tuple[int, int]:
        return (np.random.randint(0, self.N[0]), np.random.randint(0, self.N[1]))
