"""Version of the code using integers. Less general, more speed"""

import numpy as np
from scipy.sparse import linalg
import logging

from fractal_drum.int_version import lattice, eigensys
from fractal_drum.utils import plot, save, load

def main(l: int, sub: int):

    logging.info("Starting fractal setup")
    boundary = lattice.fractal(l, sub, dtype=np.uint16)
    n = lattice.calc_n(l, sub)
    #plot.is_inside(grid)
    logging.debug(f"Boundary points: {boundary.shape[1]}")
    logging.debug(f"{n = }")
    logging.info("Fractal setup complete")

    logging.info("Attemting to open stored data")
    data = load.eigen(l, sub)

    if data is None:
        logging.info("Starting matrix setup")
        A = eigensys.matrix_without_boundary(n)
        grid = lattice.lattice(boundary, sub)
        A = eigensys.apply_boundary(A, grid)
        logging.debug(f"Matrix size: {n*n}x{n*n}")
        logging.debug(f"Non-zero values: {A.nnz}")
        logging.info("Matrix setup complete")

        logging.info("Starting to solve the eigensystem")
        vals, vecs = linalg.eigsh(A, k = 100)
        logging.info("Finished solving the eigensystem")
        
        logging.info("Saving the result")
        save.eigen(l, sub, vecs, vals)
        logging.info("Saving complete")
    else:
        vecs, vals = data
        logging.info("Stored data found, using that instead of re-calculating")

    vals *= -1
    vals **= 0.5
    
    logging.info("Starting to make figures")
    plot.eigenmodes(n, vecs, vals, boundary)
    logging.info("Finished making figures")
