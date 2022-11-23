import numpy as np
import numba
from matplotlib import pyplot as plt
from matplotlib import animation
from typing import List, Tuple
from mpl_toolkits.mplot3d import Axes3D


# TODO add constants up here


@numba.jit(nopython = True)
def force(points: np.array, i: int)-> np.array:
    """calculate the force on point[i] from all other points

    Args:
        points (np.array): list of points, shape (n, 3)
        i (int): index of point to calculate forces on

    Returns:
        np.array: force vector, shape (3,)
    """
    p = points[i]
    points = np.delete(points, [3*i + j for j in range(3)]).reshape(points.shape[0] -1, 3)

    epsilon = 40
    sigma = 0.5
    mass = 1
    epsilon_0 = 1
    q = 1
    G = 1

    f = np.array([.0, .0, .0])
    for _p in points:
        d = _p - p 
        r = np.linalg.norm(d)
        #LJ_force = 24*epsilon/mass*((sigma/r)**7 - 2*(sigma/r)**13)
        LJ_force = 0
        col_force = 0
        gravity = G*mass / r**2
        f += (LJ_force + col_force + gravity)*(d/r)
    return f.astype(np.float32)


@numba.jit(nopython = True)
def ode_solver(x0: float, xend: float, y0: np.array, h: float) -> np.array:
    """solve the following system of ODEs:

    y_1' = y_2
    y_2' = sum(force(y_1, i) for i in range(len(y_1)))

    i.e. the force on each particle from all other particles.
    y can have any shape

    Args:
        x0 (float): initial x-value
        xend (float): final x-value
        y0 (np.array): initial y-values
        h (float): step size

    Returns:
        np.array: y values for the solution
    """

    # Runge-Kutta setup
    a = np.zeros((4, 4), dtype = np.float32)
    # has to be done this way with 2D arrays, sadly
    a[0] = [0, 0, 0, 0]
    a[1] = [1/2, 0, 0, 0]
    a[2] = [0, 3/4, 0, 0]
    a[3] = [2/9, 1/3, 4/9, 0]
    c = np.array([0, 1/2, 3/4, 1], dtype = np.float32)
    b = np.array([7/24, 1/4, 1/3, 1/8], dtype = np.float32)

    # Initializing:
    iterations = int((xend - x0) / h)
    y_num = np.zeros((iterations, *y0.shape), dtype=np.float32)
    y_num[0] = y0
    xn = x0
    yn = y0.astype(np.float32)
    

    for n in range(1, iterations): # Buffer for truncation errors 
        # The Runge-Kutta implementation is directly in the for loop, to make it work with jit
        k = np.zeros((len(c), *yn.shape), dtype=np.float32)
        k[0, 0] = yn[1]
        for i in range(yn.shape[1]):
            k[0, 1, i] = force(yn[0], i)
        for i in range(1, len(c)):
            tmp_y = yn
            for j in range(k.shape[0]):
                tmp_y += h*a[i,j]*k[j]
            k[i, 0] = tmp_y[1]
            for j in range(yn.shape[1]):
                k[i, 1, j] = force(tmp_y[0], j)

        add = np.zeros(k.shape)
        for i in range(k.shape[0]):
            add[i]= b[i]*k[i]
        yn += h*np.sum(add, axis = 0)
        xn += h

        y_num[n] = yn
        print(f"\r{n/iterations*100}%", end = "\r")
        
    return y_num


def animate(data):

    def animate_scatters(iteration, data, scatters):
        for i in range(data[0].shape[0]):
            scatters[i]._offsets3d = (data[iteration][i,0:1], data[iteration][i,1:2], data[iteration][i,2:])
        return scatters
    
    numDataPoints = max(data.shape)

    fig = plt.figure()
    ax = Axes3D(fig)
    
    # initiate scatterplots
    scatters = [ax.scatter(*data[0][i,:]) for i in range(data[0].shape[0])]
    
    ax.set_xlabel('X(t)')
    ax.set_ylabel('Y(t)')
    ax.set_zlabel('Z(t)')
    
    # Creating the Animation object
    anime = animation.FuncAnimation(
        fig, 
        animate_scatters, 
        frames=numDataPoints, 
        fargs=(data,scatters), 
        interval=1000//60, 
        blit=False
        )
    
    writer = animation.FFMpegWriter(fps = 60)
    
    anime.save('gravity.mp4', writer=writer)

# compile stuff
ode_solver(
    0,
    0.5,
    np.array([
        np.random.rand(3, 3)*4,
        np.zeros((3, 3))
    ]),
    0.1
)

n_particles = 5000
np.random.seed(42)
init_pos = np.random.rand(n_particles, 3)*60
init_speed = np.random.rand(n_particles, 3)#np.zeros((n_particles, 3))
init = np.array([init_pos, init_speed])

print("Creating data...")
r = ode_solver(0, 1, init, 0.001)
print("Data created")
print("Saving video...")
animate(r[::10, 0, :, :])
print("Video created")
