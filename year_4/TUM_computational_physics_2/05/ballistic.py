import numpy as np
import numba
from matplotlib import pyplot as plt
from box_count import rasterize, box_fraction

L = 256

@numba.njit
def iterate(state: np.ndarray):
    r = np.random.randint(0, L)
    state[r] += 1
    if state[r] < state[r - 1]:
        state[r] = state[r - 1]
    if state[r] < state[(r + 1) % L]:
        state[r] = state[(r + 1) % L]

@numba.njit
def mainloop(state: np.ndarray, N: int):
    for _ in range(N):
        iterate(state)
    
def main():
    s = np.zeros(L, dtype=np.uint64)
    
    mainloop(s, 10)
    for _ in range(1_000):
        mainloop(s, 1_000_000)
        s -= np.min(s)

    # Probably enough with a billion iterations
    plt.figure()
    plt.scatter(np.arange(L), s)
    plt.show()

    # Now to determine the fractal dimension
    points = np.empty((2, L), dtype=np.float64)
    for i in range(L):
        points[0, i] = s[i] / np.max(s)
        points[1, i] = i / L

    d = []
    boxes = np.logspace(1, 12, 30, endpoint=True, base=2, dtype=np.int64)

    for boxcount in boxes:
        d.append(box_fraction(points, boxcount))

    slope = np.polyfit(np.log2(boxes), np.log2(d), deg=1)
    slope = slope[0]

    plt.figure()
    plt.loglog(boxes, d)
    plt.xlabel("Boxcount")
    plt.ylabel("Box population fraction")
    plt.legend([f"{slope = :.2f} => dim = {2 + slope :.2f}"])
    plt.show()
    

if __name__ == "__main__":
    main()
