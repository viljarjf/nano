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
    for _ in range(1_0):
        mainloop(s, 1_000_000)
        s -= np.min(s)
    s += 1

    # Probably enough with a billion iterations
    # Now to determine the fractal dimension
    points_x = []
    points_y = []
    si = s[-1]
    smax = np.max(s)
    for i in range(L):
        y = [j for j in range(si, s[i], 1 if s[i] > si else -1)] + [s[i]]
        x = [i if s[i] > si else i-1 for _ in y[:-1]] + [i]
        points_y += y
        points_x += x
        si = s[i]
    
    points = np.array([points_y, points_x], dtype=np.float64)

    plt.figure()
    plt.scatter(points[1, :], points[0, :])
    plt.scatter(np.arange(L), s, marker="x", c="r")
    plt.show(block=True)

    points[0, :] /= smax
    points[1, :] /= L

    plt.figure()
    plt.imshow(rasterize(points, (256, 256)), origin="lower")
    plt.show(block=False)

    d = []
    boxes = np.logspace(2, 4, 30, endpoint=True, base=2, dtype=np.int64)

    for boxcount in boxes:
        d.append(box_fraction(points, boxcount))

    slope = np.polyfit(np.log2(boxes), np.log2(d), deg=1)
    slope = slope[0]

    plt.figure()
    plt.loglog(boxes, d)
    plt.xlabel("Boxcount")
    plt.ylabel("Box population fraction")
    plt.legend([f"{slope = :.2f} => dim = {2 + slope :.2f}"])
    plt.show(block=True)
    

if __name__ == "__main__":
    main()
