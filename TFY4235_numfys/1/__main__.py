from . import generate, properties

from matplotlib import pyplot as plt
import numpy as np

def main():
    start = np.array([[0, 1, 1, 0], [0, 0, 1, 1]], dtype = np.float32)

    new = start
    l = 4
    for i in range(l):
        new = generate.generate_next_level(new)
        print(f"Iteration {i+1} done")

    new = np.hstack((new, [[new[0, 0]], [new[1,0]]]))
    plt.plot(new[0, :], new[1, :], c = "b")

    n = new.shape[1]
    trans = np.zeros((2, n))
    """
    for i in range(n):
        trans[:, i:i+1] = generate.reverse_iteration(
            new[:, i].reshape(2, 1), 
            start[:, 0].reshape(2, 1), 
            start[:,-1].reshape(2, 1), 
            1
        )
    
    plt.plot(trans[0, :], trans[1, :], c = "r")
    for i in range(n):
        trans[:, i:i+1] = generate.reverse_iteration(
            new[:, i].reshape(2, 1), 
            start[:, 0].reshape(2, 1), 
            start[:,-1].reshape(2, 1), 
            2
        )
    plt.plot(trans[0, :], trans[1, :], c = "g")
    for i in range(n):
        trans[:, i:i+1] = generate.reverse_iteration(
            new[:, i].reshape(2, 1), 
            start[:, 0].reshape(2, 1), 
            start[:,-1].reshape(2, 1), 
            3
        )
    """
    plt.plot(trans[0, :], trans[1, :], c = "y")

    plt.plot([0, 1/3, 1, 2/3, 0], [0, 1/3, 0, -1/3, 0], c = "k")
    plt.plot([0, 1/3, 0, -1/3, 0], [0, 2/3, 1, 1/3, 0], c = "k")
    plt.plot([0, 1/3, 1, 2/3, 0], [1, 4/3, 1, 2/3, 1], c = "k")
    plt.plot([1, 4/3, 1, 2/3, 1], [0, 2/3, 1, 1/3, 0], c = "k")
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