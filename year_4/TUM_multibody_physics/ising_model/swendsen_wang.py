import numpy as np
from matplotlib import pyplot as plt
import numba
from numba import prange, float32, int32, int8
from scipy import sparse as sp

spec = {
    "J": float32,
    "Lx": int32,
    "Ly": int32,
    "bond_indices": int32[:, :],
    "spins": int8[:, :],
    "bonds": int8[:],
}

# Compiling takes a lot of time, so it is not that much of a speedup.
@numba.experimental.jitclass(spec)
class System:

    def __init__(self, J: float, Lx: int, Ly: int, initial_state: np.ndarray = None):
        self.J = J
        self.Lx = Lx
        self.Ly = Ly

        # Initialize bond indices
        self.bond_indices = np.empty((2*self.N, 2), dtype=np.int32)
        for n in range(self.N):
            x, y = self.idx_2_xy(n)
            # left-right
            self.bond_indices[2*n, 0] = n
            self.bond_indices[2*n, 1] = self.xy_2_idx(x, (y + 1) % self.Ly)
            # up-down
            self.bond_indices[2*n + 1, 0] = n
            self.bond_indices[2*n + 1, 1] = self.xy_2_idx((x + 1) % self.Lx, y)

        # Set random initial state if not given.
        # Numba does not support many array operations,
        # so this algorithm is dumbed down a lot.
        self.spins = np.ones(self.shape, dtype=np.int8)
        if initial_state is None:
            for n in prange(self.N):
                if np.random.random() < 0.5:
                    y, x = self.idx_2_xy(n)
                    self.spins[y, x] = -1
        else:
            self.spins = initial_state

        self.bonds = np.zeros(2*self.N, dtype=np.int8)
            
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
    
    def get_spin(self, idx: int) -> int:
        return self.spins[self.idx_2_xy(idx)]
    
    def update_bonds(self, kbT: float):
        for i, (spin_1, spin_2) in enumerate(self.bond_indices):
            # equal spins: no bond
            if self.get_spin(spin_1) != self.get_spin(spin_2):
                self.bonds[i] = 0
            # Different spins: 1 with probability e^-beta*J
            else:
                self.bonds[i] = np.random.random() > np.exp(-self.J / kbT)
    
    def flip_clusters(self, n_clusters: int, clusters: np.ndarray):
        # pre-determine which clusters to flip
        clusters_to_flip = np.random.random(n_clusters) < 0.5
        # loop through all the spins
        for idx in prange(self.N):
            # check if it should be flipped
            if clusters_to_flip[clusters[idx]]:
                # flip
                self.spins[self.idx_2_xy(idx)] *= -1
    
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