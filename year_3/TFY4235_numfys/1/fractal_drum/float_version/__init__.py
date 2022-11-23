"""Version of the code using floats"""

from fractal_drum.float_version import generate, properties
from fractal_drum.utils import plot

import numpy as np
#from scipy.sparse import linalg
from cupyx.scipy.sparse import linalg
import cupy
import logging

def main():    
    start = np.array([[0, 1, 1, 0], [0, 0, 1, 1]], dtype = np.float32)
    l = 5

    new = start
    for i in range(l):
        new = generate.next_level(new)
        logging.debug(f"Iteration {i+1} done")
        
    # not strictly necessary, but compiling the function doesn't hurt
    properties.is_inside(np.array([0.59375, 0.03125]), start)

    lattice = generate.lattice(start, l)
    
    logging.info("Starting matrix setup")

    n = lattice.shape[1]
    A = generate.sparce_matrix(lattice, start)
    h = np.linalg.norm(start[:, 1] - start[:, 0]) / n

    A = cupy.sparse.csc_matrix(A)
    #A = A.asformat("coo")

    logging.info("Finished matrix setup")
    
    logging.info("Starting to solve the eigenproblem")
    
    gpu_eigenvals, gpu_v = linalg.eigsh(A, k = 10, which = "LM")
    eigenvals = gpu_eigenvals.get()
    v = gpu_v.get()
    #eigenvals, v = linalg.eigsh(A, k = 10, sigma = 0)
    
    logging.info("Finished solving the eigenproblem")
    eigenvals *= -h**2
    eigenvals **= 0.5

    logging.info("Starting to make figures")
    plot.eigenmodes(n, v, eigenvals, lattice)
    logging.info("Finished making figures")