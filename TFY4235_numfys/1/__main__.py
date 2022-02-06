from . import generate, properties, utils

from matplotlib import pyplot as plt
import numpy as np

def main():
    start = np.array([[0, 1, 1, 0], [0, 0, 1, 1]], dtype = np.float32)

    new = start
    l = 2
    for i in range(l):
        new = generate.generate_next_level(new)
        print(f"Iteration {i+1} done")

    new = np.hstack((new, [[new[0, 0]], [new[1,0]]]))
    lattice = generate.generate_lattice(start, l+1)
    l_pts = lattice.shape[1]
    for i in range(lattice.shape[1]):
        if properties.is_inside(lattice[:, i], start) == -1:
            lattice[:, i] = [0, 0]
            l_pts -= 1
    
    print(f"corners: {new.shape[1]}\ncount: {l_pts}\nfraction: {l_pts / new.shape[1] * 100 :.1f}%")

    plt.plot(new[0, :], new[1, :], c = "b")
    plt.scatter(lattice[0, :], lattice[1, :], c = "g")
    plt.show()

    x = np.linspace(0.1, 0.2, 1024)
    y = np.linspace(0.4, 0.5, 1024)
    xx, yy = np.meshgrid(x, y)

    zz = xx.copy()
    p = np.array([xx, yy])
    for i in range(xx.shape[0]):
        for j in range(xx.shape[1]):
            zz[i, j] = properties.is_inside(p[:, i, j], start)
    print(np.count_nonzero(zz == 0))
    plt.pcolormesh(x, y, zz, shading="auto")
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