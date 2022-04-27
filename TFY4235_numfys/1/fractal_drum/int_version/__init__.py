"""Version of the code using integers. Less general, more speed"""

import numpy as np
from scipy.sparse import linalg
import logging

from fractal_drum.int_version import lattice, eigensys
from fractal_drum.utils import plot, save, load, fractal_dimension

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
        A, ind = eigensys.apply_boundary(A, grid)
        logging.debug(f"Matrix size: {n*n}x{n*n}")
        logging.debug(f"Pruned matrix size: {A.shape[0]}x{A.shape[1]}")
        logging.debug(f"Non-zero values: {A.nnz}")
        logging.info("Matrix setup complete")
        logging.info("Starting to solve the eigensystem")
        vals, _vecs = linalg.eigsh(A, k = 500, sigma = 0)
        vals = vals[::-1]
        _vecs = _vecs[:, ::-1]
        vecs = np.zeros((n**2, _vecs.shape[1]), dtype=_vecs.dtype)
        for i in range(_vecs.shape[1]):
            vecs[:, i] = eigensys.fill_eigenvector(l, sub, _vecs[:, i], ind)
        logging.info("Finished solving the eigensystem")
        
        logging.info("Saving the result")
        save.eigen(l, sub, vecs, vals)
        logging.info("Saving complete")
    else:
        vecs, vals = data
        logging.info("Stored data found, using that instead of re-calculating")

    vals *= -(4**l*sub)**2
    vals **= 0.5
    
    logging.info("Starting to make figures")
    plot.eigenmodes(n, vecs, vals, boundary, amount=10)
    logging.info("Finished making figures")
    
    logging.info("Calculating fractal dimension")
    dNs = []
    Ns = []
    for omega in vals:
        Ns.append(fractal_dimension.N(vals, omega))
        dNs.append(fractal_dimension.dN(vals, omega))
    dNs = np.array(dNs)
    Ns = np.array(Ns)
    d, _ = fractal_dimension.d(vals, dNs)
    d, k = d
    logging.debug(f"{d = }")
    plot.idos(vals, Ns)
    plot.weyl_berry_conjecture(vals, dNs, d, k)

    logging.info("Fractal dimension calculation complete")

