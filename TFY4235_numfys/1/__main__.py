from . import generate, properties, utils

from matplotlib import pyplot as plt
import numpy as np

def main():
    start = np.array([[0, 1, 1, 0], [0, 0, 1, 1]], dtype = np.float32)
    single_line = np.array([[0, 12], [0, 0]], dtype = np.float32)

    new = start
    l = 6
    for i in range(l):
        new = generate.generate_next_level(new)
        print(f"Iteration {i+1} done")

    new = np.hstack((new, [[new[0, 0]], [new[1,0]]]))
    plt.plot(new[0, :], new[1, :], c = "b")

    print(properties.is_inside(np.array([0.7, 0.33]), start))
    plt.show()
    
    return
    dist = []
    for i in range(lattice.shape[1]):
        dist.append(properties.distance_estimate(lattice[:, i], start, l))
    dist = np.array(dist).reshape(int(lattice.shape[1]**0.5), int(lattice.shape[1]**0.5))
    
    plt.pcolormesh(np.unique(lattice[0, :]), np.unique(lattice[1, :]), dist)
    plt.colorbar()
    plt.show()

if __name__ == "__main__":
    main()