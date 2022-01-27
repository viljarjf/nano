from . import generate

from matplotlib import pyplot as plt
import numpy as np

def main():
    start = np.array([[0, 0, 1, 1], [0, 1, 1, 0]], dtype = np.float32)

    new = start
    l = 1
    for i in range(l):
        new = generate.generate_next_level(new)
        print(f"Iteration {i+1} done")
    new = np.hstack((new, [[new[0, 0]], [new[1,0]]]))
    plt.plot(new[0, :], new[1, :])

    lattice = generate.generate_lattice(start, l + 1)
    plt.scatter(lattice[0, :], lattice[1, :])

    plt.show()

if __name__ == "__main__":
    main()