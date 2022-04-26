"""Version of the code using integers. Less general, more speed"""

import numpy as np
from scipy.sparse import linalg
import os
import logging

from fractal_drum.int_version import lattice, eigensys
from fractal_drum.utils import plot

def main():
    logging.info("Starting fractal setup")
    boundary = lattice.fractal(4, dtype=np.uint16)
    grid = lattice.lattice(boundary, 2)
    n = grid.shape[0]
    #plot.is_inside(grid)
    logging.debug(f"Boundary points: {boundary.shape[1]}")
    logging.debug(f"{n = }")
    logging.info("Fractal setup complete")

    logging.info("Starting matrix setup")
    A = eigensys.matrix_without_boundary(n)
    A = eigensys.apply_boundary(A, grid)
    logging.debug(f"Matrix size: {n*n}x{n*n}")
    logging.debug(f"Non-zero values: {A.nnz}")
    logging.info("Matrix setup complete")
    
    logging.info("Starting to solve the eigensystem")
    eigenvals, v = linalg.eigsh(A, k = 20)
    logging.info("Finished solving the eigensystem")
    
    eigenvals *= -1
    eigenvals **= 0.5
    
    logging.info("Starting to make figures")
    plot.eigenmodes(n, v, eigenvals, boundary)
    logging.info("Finished making figures")
