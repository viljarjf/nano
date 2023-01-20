from __future__ import annotations
"""

Custom class to hopefully speed up hamiltonian addition

"""
from scipy import sparse as sp
import numpy as np

class Hamiltonian(sp.dia_matrix):

    def add_static_potential(self, V0: np.ndarray):
        self.__default_data = self.data
        self.__default_data[1, :] += V0
    
    def add(self, potential) -> Hamiltonian:
            self.data = self.__default_data
            # index 1 is the central diagonal
            self.data[1, :] += potential
            return self
