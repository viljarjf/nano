import numpy as np
import numba
import sympy
from matplotlib import pyplot as plt
from matplotlib import animation
from typing import List
from scipy.optimize import fsolve
from mpl_toolkits.mplot3d import Axes3D
                

class RungeKutta:
    def __init__(self, c, a, b, p=0, is_explicit = True):
        self.a = np.array(a)
        self.c = np.array(c)
        self.b = np.array(b)
        self.p = p
        self.prev_k = None
        self.is_explicit = is_explicit

    def __call__(self, f, xn, yn, h):
        k_shape = (len(self.c), *yn.shape)

        def func(kn):
            s = kn.shape
            kn = kn.reshape(k_shape)
            yf = list()
            for i in range(len(kn)):
                xl = xn + h*self.c[i]
                l = list()
                for j in range(len(self.c)):
                    l.append(self.a[i, j]*kn[j])
                yl = yn + h*np.sum(np.array(l), axis = 0)
                val = f(xl, yl)
                yf.append(val)
            return (kn - np.array(yf)).reshape(s)
        if not self.is_explicit:
            if self.prev_k is None:
                k = np.array(fsolve(func, np.ones(k_shape))).reshape(k_shape)
            else:
                k = np.array(fsolve(func, self.prev_k)).reshape(k_shape)
        else:
            k = [f(xn, yn)]
            for i in range(1, len(self.c)):
                tmp_x = xn + self.c[i]*h
                tmp_y = h*np.sum([self.a[i, j]*k[j] for j in range(len(k))], axis = 0)
                k.append(f(tmp_x, yn + tmp_y))
            k = np.array(k)
        self.prev_k = k
        if len(k) == 1:
            add = self.b[0]*k[0]
        else:
            add = np.sum([self.b[j]*k[j] for j in range(len(k))], axis = 0)
        y_next = yn + h*add
        x_next = xn + h
        return x_next, y_next


def ode_solver(f, x0, xend, y0, h, method):
    '''
    Generic solver for ODEs
       y' = f(x,y), y(a)=y0
    Input: f, the integration interval x0 and xend, 
           the stepsize h and the method of choice.  
      
    Output: Arrays with the x- and the corresponding y-values. 
    '''
    
    # Initializing:
    y_num = np.array([y0])
    x_num = np.array([x0])

    xn = x0
    yn = np.array(y0) 

    while xn < xend - 1.e-10: # Buffer for truncation errors        
        xn, yn = method(f, xn, yn, h)

        y_num = np.concatenate((y_num, np.array([yn])))
        x_num = np.append(x_num,xn)
        
    return x_num, y_num


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

    epsilon = 4
    sigma = 0.7
    mass = 1
    epsilon_0 = 1

    f = np.array([.0, .0, .0])
    for _p in points:
        d = _p - p 
        r = np.linalg.norm(d)
        LJ_force = 24*epsilon/mass*((sigma/r)**7 - 2*(sigma/r)**13)
        
        col_force = 0
        f += (LJ_force + col_force)*(d/r)
    return f


def particle_func(t, r):
    return np.array([
        r[1],
        np.array([force(r[0], i) for i in range(r.shape[1])])
    ])

n_particles = 5
np.random.seed(1)
init_speed = np.zeros((n_particles, 3))
init_pos = np.random.rand(n_particles, 3)*4
init = np.array([init_pos, init_speed])

c = [0, 1/2, 3/4, 1]
a = np.array([
    [0, 0, 0, 0],
    [1/2, 0, 0, 0],
    [0, 3/4, 0, 0],
    [2/9, 1/3, 4/9, 0]
    ])
b = [7/24, 1/4, 1/3, 1/8]
rkp = RungeKutta(c, a, b, is_explicit=True)
t, r = ode_solver(particle_func, 0, 5, init, 0.01, rkp)


def animate(data = None):
    """data: shape (l, 3, n) for l lines, and n timesteps
    """
    def animate_scatters(iteration, data, scatters):
        for i in range(data[0].shape[0]):
            scatters[i]._offsets3d = (data[iteration][i,0:1], data[iteration][i,1:2], data[iteration][i,2:])
        return scatters
    
    if data is None:
        # THE DATA POINTS
        z = np.arange(0,1,0.001)
        x = np.cos(z*50)
        y = np.sin(z*50)
        dataSet = np.array([x, y, z])
        dataSet2 = np.array([x, -y, 1-z])

        dataSets = []
        dataSets.append(dataSet)
        dataSets.append(dataSet2)
        data = np.array(dataSets)
    numDataPoints = max(data.shape)
    # GET SOME MATPLOTLIB OBJECTS
    fig = plt.figure()
    ax = Axes3D(fig)
    
    # NOTE: Can't pass empty arrays into 3d version of plot()
    scatters = [ax.scatter(*data[0][i,:]) for i in range(data[0].shape[0])]
    
    # AXES PROPERTIES]
    # ax.set_xlim3d([limit0, limit1])
    ax.set_xlabel('X(t)')
    ax.set_ylabel('Y(t)')
    ax.set_zlabel('Z(t)')
    
    # Creating the Animation object
    line_anime = animation.FuncAnimation(
        fig, 
        animate_scatters, 
        frames=numDataPoints, 
        fargs=(data,scatters), 
        interval=1, 
        blit=False
        )
    
    plt.show()
animate(r[:, 0, :, :])