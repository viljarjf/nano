"""
Shared codebase for ising model
"""

import numpy as np
from matplotlib import pyplot as plt
import numba
from numba import prange, njit
from scipy import sparse as sp


class IsingModel:

    def __init__(self, J: float, Lx: int, Ly: int, initial_state: np.ndarray = None):
        self.J = J
        self.Lx = Lx
        self.Ly = Ly

        # Initialize bond indices
        self.init_bond_indices()
    
        # Set random initial state if not given.
        if initial_state is None:
            self.spins = self.get_random_spin_state()
        else:
            # TODO check input for shape, dtype ect
            self.spins = initial_state.flatten()

        self.bonds = np.zeros(2*self.N, dtype=np.int8)


    @staticmethod
    @njit(parallel=True)
    def __jit_get_random_spin_state(N: int) -> np.ndarray:
        # Numba does not support many array operations,
        # so this algorithm is dumbed down a lot.
        spins = np.ones(N, dtype=np.int8)
        for n in prange(N):
            if np.random.random() < 0.5:
                spins[n] = -1
        return spins
    
    def get_random_spin_state(self):
        return self.__jit_get_random_spin_state(self.N)


    @staticmethod
    @njit(parallel=True)
    def __jit_get_init_bond_indices(shape: tuple[int]) -> np.ndarray:
        Ly, Lx = shape
        N = Lx * Ly

        def xy_2_idx(x: int, y: int) -> int:
            return Ly * x + y
    
        def idx_2_xy(idx: int) -> tuple[int, int]:
            return divmod(idx, Ly)  
        
        bond_indices = np.empty((2*N, 2), dtype=np.int32)
        for n in prange(N):
            x, y = idx_2_xy(n)
            # left-right
            bond_indices[2*n, 0] = n
            bond_indices[2*n, 1] = xy_2_idx(x, (y + 1) % Ly)
            # up-down
            bond_indices[2*n + 1, 0] = n
            bond_indices[2*n + 1, 1] = xy_2_idx((x + 1) % Lx, y)
        return bond_indices
    
    def init_bond_indices(self):
        self.bond_indices = self.__jit_get_init_bond_indices(self.shape)
            

    @staticmethod
    @njit(parallel=True)
    def __jit_update_bonds(J: int, kbT: float, bonds: np.ndarray, spins: np.ndarray, 
                           bond_indices: np.ndarray) -> np.ndarray:
        # I don't know any parallel equivalent of enumerate, use this instead
        for i in prange(bond_indices.shape[0]):
            spin_1, spin_2 = bond_indices[i]
            # equal spins: no bond
            if spins[spin_1] != spins[spin_2]:
                bonds[i] = 0
            # Different spins: 1 with probability e^-2beta*J
            else:
                bonds[i] = np.random.random() > np.exp(-2*J / kbT)

    def update_bonds(self, kbT: float):
        self.__jit_update_bonds(self.J, kbT, self.bonds, self.spins, self.bond_indices) 
    

    def find_clusters(self) -> np.ndarray:
        # Create sparse matrix from spins
        graph = sp.csr_matrix(
            (self.bonds, (self.bond_indices[:, 0], self.bond_indices[:, 1])),
            dtype=np.int8,
            shape=(self.N, self.N)
            )
        graph.eliminate_zeros()
        # Add the transpose to make bonds two-way
        graph += graph.T
        # Find the connections
        n_connections, connections = sp.csgraph.connected_components(graph)
        return connections
    

    @staticmethod
    @njit(parallel=True)
    def __jit_flip_clusters(N: int, spins: np.ndarray, clusters: np.ndarray):
        # pre-determine which clusters to flip
        clusters_to_flip = np.random.random(clusters.shape[0]) < 0.5
        # loop through all the spins
        for idx in prange(N):
            # check if it should be flipped
            if clusters_to_flip[clusters[idx]]:
                # flip
                spins[idx] *= -1
    
    def flip_clusters(self, clusters: np.ndarray):
        self.__jit_flip_clusters(self.N, self.spins, clusters)
    

    def find_and_flip_clusters(self):
        clusters = self.find_clusters()
        self.flip_clusters(clusters)


    def show_clusters(self, clusters: np.ndarray) -> np.ndarray:
        out = np.empty(self.shape)
        for idx in prange(self.N):
            out[self.idx_2_xy(idx)] = clusters[idx]
        return out
    

    @staticmethod
    @njit
    def __jit_iterate_metropolis(shape: tuple[int], spins: np.ndarray, J: float, 
                                 kbT: float, flips: int, equilibrium_flips: int):
        Ly, Lx = shape
        N = Lx * Ly

        def xy_2_idx(x: int, y: int) -> int:
            return Ly * x + y
    
        def idx_2_xy(idx: int) -> tuple[int, int]:
            return divmod(idx, Ly) 

        for _ in range(equilibrium_flips + flips):

            idx = np.random.randint(N)
            x, y = idx_2_xy(idx)

            # Measure change in energy of flipping chosen site
            neighbours =   (spins[xy_2_idx(x, (y + 1) % Ly)] + # down
                            spins[xy_2_idx(x, (y - 1) % Ly)] + # up
                            spins[xy_2_idx((x + 1) % Lx, y)] + # right
                            spins[xy_2_idx((x - 1) % Lx, y)])  # left     
            # dE = -2 * Energy at site x, y
            # Energy at site = -J * sum(spin_xy * spin_neighbour) 
            # => dE = -2 * (-J) * spin_xy * sum(neighbours)
            dE =  2 * J * spins[idx] * neighbours 

            # e^-dE when dE < 0 is always greater than 1.
            # Therefore, this if-statement captures the dE < 0 condition to flip
            if np.exp(-dE / kbT) > np.random.rand():
                spins[idx] *= -1
            
    def iterate_metropolis(self, kbT: float, flips: int, equilibrium_flips: int = 0):
        self.__jit_iterate_metropolis(self.shape, self.spins, self.J, kbT, flips, equilibrium_flips)


    def iterate_swendsen_wang(self, kbT: float):
        self.update_bonds(kbT)
        self.find_and_flip_clusters()


    @staticmethod
    @njit
    def __jit_measure_energy(J: float, spins: np.ndarray, bond_indices: np.ndarray) -> float:
        out = 0
        for spin_1, spin_2 in bond_indices:
            if spins[spin_1] != spins[spin_2]:
                out += J
            else:
                out -= J
        return out

    def xy_2_idx(self, x: int, y: int) -> int:
        return self.Ly * x + y
    
    def idx_2_xy(self, idx: int) -> tuple[int, int]:
        return divmod(idx, self.Ly)  

    @property
    def spin_array(self):
        return self.spins.reshape(self.shape)  
    
    @property
    def N(self) -> int:
        return self.Lx * self.Ly
    
    @property
    def shape(self) -> tuple[int, int]:
        return self.Ly, self.Lx
    
    
    @property
    def E(self) -> float:
        return self.__jit_measure_energy(self.J, self.spins, self.bond_indices)
    
    @property
    def M(self) -> float:
        return np.mean(self.spins)
