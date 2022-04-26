"""Version of the code using integers. Less general, more speed"""

import numpy as np
from scipy.sparse import linalg
import os
import logging

from fractal_drum.int_version import lattice, eigensys
from fractal_drum.utils import plot

def main():
    logging.info("Starting matrix setup")
    a = lattice.fractal(4, dtype=np.uint16)
    b = lattice.lattice(a, 2)
    n = b.shape[0]
    A = eigensys.matrix_without_boundary(n)
    A = eigensys.apply_boundary(A, b)
    logging.info("Matrix setup complete")

    logging.info("Starting to solve the eigensystem")
    eigenvals, v = linalg.eigsh(A, k = 20)
    logging.info("Finished solving the eigensystem")
    
    eigenvals *= -1
    eigenvals **= 0.5
    
    logging.info("Starting to make figures")
    plot.eigenmodes(n, v, eigenvals, a)
    logging.info("Finished making figures")
