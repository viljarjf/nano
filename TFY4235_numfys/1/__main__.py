from . import generate

from matplotlib import pyplot as plt
import numpy as np

def main():
    start = np.array([[0, 1], [0, 0]], dtype = np.float64)

    new = start
    for i in range(8):
        new = generate.generate_next_level(new)
        print(f"Iteration {i+1} done")
    plt.plot(new[0, :], new[1, :])
    plt.show()

if __name__ == "__main__":
    main()