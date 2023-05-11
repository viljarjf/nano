import numpy as np
from matplotlib import pyplot as plt
import numba
from numba import prange, njit
from scipy import sparse as sp


class System:

    def __init__(self, J: float, Lx: int, Ly: int, initial_state: np.ndarray = None):
        self.J = J
        self.Lx = Lx
        self.Ly = Ly

        # Initialize bond indices
        self.bond_indices = self.__jit_init_bond_indices(self.shape)
    
        # Set random initial state if not given.
        if initial_state is None:
            self.spins = self.__jit_init_state_random(self.shape)
        else:
            # TODO check input for shape, dtype ect
            self.spins = initial_state.flatten()

        self.bonds = np.zeros(2*self.N, dtype=np.int8)

    @staticmethod
    @njit(parallel=True)
    def __jit_init_state_random(N: int) -> np.ndarray:
        # Numba does not support many array operations,
        # so this algorithm is dumbed down a lot.
        spins = np.ones(N, dtype=np.int8)
        for n in prange(N):
            if np.random.random() < 0.5:
                spins[n] = -1
        return spins

    @staticmethod
    @njit(parallel=True)
    def __jit_init_bond_indices(shape: tuple[int]) -> np.ndarray:
        Ly, Lx = shape
        N = Lx * Ly
        bond_indices = np.empty((2*N, 2), dtype=np.int32)
        for n in range(N):
            # left-right
            bond_indices[2*n, 0] = n
            bond_indices[2*n, 1] = (n + 1) % Lx
            # up-down
            bond_indices[2*n + 1, 0] = n
            bond_indices[2*n + 1, 1] = (n + Lx) % N
        return bond_indices
            
    @property
    def N(self) -> int:
        return self.Lx * self.Ly
    
    @property
    def shape(self) -> tuple[int, int]:
        return self.Ly, self.Lx
    
    def xy_2_idx(self, x: int, y: int) -> int:
        return self.Ly * x + y
    
    def idx_2_xy(self, idx: int) -> tuple[int, int]:
        return divmod(idx, self.Ly)    

    @staticmethod
    @njit(parallel=True)
    def __jit_update_bonds(kbT: float, spins: np.ndarray, bond_indices: np.ndarray) -> np.ndarray:
        N_bonds = bond_indices.shape[0]
        bonds = np.empty(N_bonds, dtype=np.int8)
        for i, (spin_1, spin_2) in enumerate(bond_indices):
            # equal spins: no bond
            if bonds[spin_1] != bonds[spin_2]:
                bonds[i] = 0
            # Different spins: 1 with probability e^-beta*J
            else:
                bonds[i] = np.random.random() > np.exp(-self.J / kbT)
    
    def flip_clusters(self, n_clusters: int, clusters: np.ndarray):
        # pre-determine which clusters to flip
        clusters_to_flip = np.random.random(n_clusters) < 0.5
        # loop through all the spins
        for idx in prange(self.N):
            # check if it should be flipped
            if clusters_to_flip[clusters[idx]]:
                # flip
                self.spins[idx] *= -1
    
    def show_clusters(self, clusters: np.ndarray) -> np.ndarray:
        out = np.empty(self.shape)
        for idx in prange(self.N):
            out[self.idx_2_xy(idx)] = clusters[idx]
        return out
    
    @property
    def E(self) -> float:
        out = 0
        for spin_1, spin_2 in self.bond_indices:
            if self.get_spin(spin_1) != self.get_spin(spin_2):
                out += self.J
            else:
                out -= self.J
        return out
    
    @property
    def M(self) -> float:
        return np.mean(self.spins)
            

# scipy is not supported in jit classes
# I can't be bothered to rewrite it now
def find_connected_components(s: System):
    graph = sp.csr_matrix(
        (s.bonds, (s.bond_indices[:, 0], s.bond_indices[:, 1])),
        dtype=np.int8,
        shape=(s.N, s.N)
        )
    graph.eliminate_zeros()
    graph += graph.T
    connections = sp.csgraph.connected_components(graph)
    return connections

def iterate_system(s: System, kbT: float):
    s.update_bonds(kbT)
    s.flip_clusters(*find_connected_components(s))