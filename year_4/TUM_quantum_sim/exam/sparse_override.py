"""

Custom class to hopefully speed up hamiltonian addition

"""
from scipy import sparse as sp
import numpy as np

class Hamiltonian(sp.dia_matrix):

    def __add__(self, other):
        if isinstance(other, np.ndarray):
            self.setdiag(self.diagonal(0) + other)
            return self
        else:
            return super().__add__(other)
