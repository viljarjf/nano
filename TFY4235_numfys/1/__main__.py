from . import generate, properties, utils

from matplotlib import pyplot as plt
import numpy as np

from scipy.sparse import linalg

def main():    
    start = np.array([[0, 1, 1, 0], [0, 0, 1, 1]], dtype = np.float32)

    new = start
    l = 4
    for i in range(l):
        new = generate.generate_next_level(new)
        print(f"Iteration {i+1} done")
    
    print(properties.is_inside(np.array([0.59375, 0.03125]), start))

    new = np.hstack((new, [[new[0, 0]], [new[1,0]]]))
    lattice = generate.generate_lattice(start, l)
    
    print("Starting matrix setup")

    n = lattice.shape[1]
    A = generate.generate_sparce_matrix(n)
    h = np.linalg.norm(start[:, 1] - start[:, 0]) / n

    for i in range(n):
        for j in range(n):
            if properties.is_inside(lattice[:, i, j], start) != 1:
                properties.set_zero(i, j, n, A)

    print("Finished marix setup")

    roots, v = linalg.eigsh(A.asformat("coo"), k = 10)
    roots *= h**2
    print(roots)
    


if __name__ == "__main__":
    main()