import numpy as np
from matplotlib import pyplot as plt

def next_point(x: float, y: float) -> tuple[float, float]:
    r = np.random.random()

    if r < 0.1:
        x = 0.05 * x
        y = 0.05 * y

    elif r < 0.2:
        x = 0.05 * x
        y = -0.5 * y + 1
    
    elif r < 0.4:
        x = 0.46 * x - 0.15 * y
        y = 0.39 * x + 0.38 * y + 0.6
    
    elif r < 0.6:
        x = 0.47 * x - 0.15 * y
        y = 0.17 * x + 0.42 * y + 1.1
    
    elif r < 0.8:
        x = 0.43 * x + 0.28 * y
        y = -0.25 * x + 0.45 * y + 1.0
    
    else:
        x = 0.42 * x + 0.26 * y
        y = -0.35 * x + 0.31 * y + 0.7
    
    return x, y

def generate(N: int) -> np.ndarray:
    points = np.empty((2, N),  dtype=np.float64)

    x, y = 0.5, 0
    for i in range(N):
        points[:, i] = x, y
        x, y = next_point(x, y)
    return points


points = generate(10000)

plt.figure()
plt.scatter(points[0, :], points[1, :])
plt.show()
