import os
from . import generate, properties, utils

from matplotlib import pyplot as plt
import numpy as np

from scipy.sparse import linalg

#os.environ["CUDA_VISIBLE_DEVICES"] = "0"
#from cupyx.scipy.sparse import linalg
#import cupy

def main():    
    start = np.array([[0, 1, 1, 0], [0, 0, 1, 1]], dtype = np.float32)
    l = 4

    new = start
    for i in range(l):
        new = generate.generate_next_level(new)
        print(f"Iteration {i+1} done")
        
    # not strictly necessary, but compiling the function doesn't hurt
    properties.is_inside(np.array([0.59375, 0.03125]), start)

    lattice = generate.generate_lattice(start, l)
    
    print("Starting matrix setup")

    n = lattice.shape[1]
    A = generate.generate_sparce_matrix(n)
    h = np.linalg.norm(start[:, 1] - start[:, 0]) / n

    for i in range(n):
        for j in range(n):
            if properties.is_inside(lattice[:, i, j], start) != 1:
                properties.set_zero(i, j, n, A)
    
    #A = cupy.sparse.coo_matrix(A)
    A = A.asformat("coo")

    print("Finished marix setup")

    print("Starting to solve the eigenproblem")
    
    #gpu_roots, gpu_v = linalg.eigsh(A, k = 100)
    #roots = gpu_roots.get()
    #v = gpu_v.get()
    roots, v = linalg.eigsh(A.asformat("coo"), k = 100)

    print("Finished solving the eigenproblem")
    roots *= -h**2
    roots **= 0.5
    
    figdir = os.path.join(os.path.dirname(__file__), "figures")
    if not os.path.exists(figdir):
        os.makedirs(figdir)

    print("Starting to make figures")
    x = np.unique(lattice[0, :, :])
    y = np.unique(lattice[1, :, :])
    for i in range(v.shape[1]):
        plt.figure(figsize = (4, 4), dpi = 250)
        plt.pcolormesh(x, y, np.transpose(v[:, i].reshape(n, n)**2))
        plt.plot(new[0, :], new[1, :], )
        plt.savefig(os.path.join(figdir, f"Eigenvector #{i}.png"), )
        plt.close()
    print("Done")

if __name__ == "__main__":
    main()