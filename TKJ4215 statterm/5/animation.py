import numpy as np
import numba
import sympy
from matplotlib import pyplot as plt
from matplotlib import animation
from typing import List
from scipy.optimize import fsolve
from mpl_toolkits.mplot3d import Axes3D


class Particle:
    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z
    
    def __str__(self):
        return f"{self.x}, {self.y}, {self.z}"


class System:

    def __init__(self, particles: List[Particle], sigma: float, epsilon: float) -> None:
        self.particles = particles

        tmp = np.array([[p.x, p.y, p.z] for p in self.particles])
        self.x = tmp[:,0]
        self.y = tmp[:,1]
        self.z = tmp[:,2]

        self.n = len(particles)
        self.s = sigma
        self.e = epsilon
        self.max_r = 3 # tested with eps = sig = 1

    def generate_forces(self) -> np.array:
        """Generate a list of force vectors corresponding to the particles in the system

        Returns:
            np.array: list of forces, (x, y, z)
        """
        #@numba.jit(nopython = True)
        def get_r_arr(n, x, y, z) -> np.array:
            """generate r matrix. 
            first index: particle index 
            second index: distance to particle at corresponding index

            Returns:
                np.array: shape (n x n), for n particles
            """
            r = np.zeros((n, n))
            for i in range(n):
                r[:, i] = ((x - x[i])**2 + (y - y[i])**2 + (y - y[i])**2)**0.5
                r[i, i] = np.nan
            return r
        
        #@numba.jit(nopython = True)
        def _generate(_n, _x, _y, _z, _e, _s, _max_r):
            f = np.zeros((3, _n, _n))
            for i in range(_n):
                f[:, i, :] = [
                    6*(_s/ (_x[i] - _x))**7 - 12*(_s / (_x[i] - _x))**13,
                    6*(_s/ (_y[i] - _y))**7 - 12*(_s / (_y[i] - _y))**13,
                    6*(_s/ (_z[i] - _z))**7 - 12*(_s / (_z[i] - _z))**13
                ]
                f *= 4*_e
            r = get_r_arr(_n, _x, _y, _z)
            #print(r)
            #print(f)
            f[:, (r>_max_r)&np.isnan(r)] *= 0
            f[np.isnan(f)] = 0
            return np.sum(f, axis = 1), r
        
        return _generate(self.n, self.x, self.y, self.z, self.e, self.s, self.max_r)
                

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

class RungeKutta_pair:
    def __init__(self, c, a, b_1, b_2, p, is_explicit):
        self.rk2 = RungeKutta(c, a, b_2, is_explicit = is_explicit)
        self.b1 = b_1
        self.b2 = b_2
        self.p = p

    def __call__(self, f, xn, yn, h):
        x_next, y_next = self.rk2(f, xn, yn, h)
        error_estimate = h*np.sum([(self.b2[i]-self.b1[i])*self.rk2.prev_k[i] for i in range(len(self.rk2.prev_k))], axis = 0)
        error_estimate = np.linalg.norm(error_estimate)
        return x_next, y_next, error_estimate, self.p


def ode_solver(f, x0, xend, y0, h, method):
    '''
    Generic solver for ODEs
       y' = f(x,y), y(a)=y0
    Input: f, the integration interval x0 and xend, 
           the stepsize h and the method of choice.  
      
    Output: Arrays with the x- and the corresponding y-values. 
    '''
    
    # Initializing:
    y_num = np.array([y0])    # Array for the solution y 
    x_num = np.array([x0])    # Array for the x-values

    xn = x0                # Running values for x and y
    yn = np.array(y0) 

    # Main loop
    while xn < xend - 1.e-10:            # Buffer for truncation errors        
        xn, yn = method(f, xn, yn, h)[:2]   # Do one step by the method of choice
        # Extend the arrays for x and y
        y_num = np.concatenate((y_num, np.array([yn])))
        x_num = np.append(x_num,xn)
        
    return x_num, y_num

def adaptive(f, x0, xend, y0, h0, pair, tol = 1.e-6):
    '''
    Adaptive solver for ODEs
       y' = f(x,y), y(x0)=y0
    
    Input: the function f, x0, xend, and the initial value y0
           intial stepsize h, the tolerance tol, 
           and a function (method) implementing one step of a pair.
    Output: Array with x- and y- values.
    '''
    
    y_num = np.array([y0])    # Array for the solutions y
    x_num = np.array([x0])    # Array for the x-values

    xn = x0                # Running values for  x, y and the stepsize h
    yn = np.array(y0) 
    h = h0
    Maxcall = 100000        # Maximum allowed calls of method
    ncall = 0
    
    # Main loop
    while xn < xend - 1.e-10:               # Buffer for truncation error
        # Adjust the stepsize for the last step
        if xn + h > xend:                   
            h = xend - xn 
        
        # Perform one step with the chosen mehtod
        x_try, y_try, error_estimate, p = pair(f, xn, yn, h)
        ncall = ncall + 1
        
        if error_estimate <= tol:   
            # Solution accepted, update x and y
            xn = x_try    
            yn = y_try
            # Store the solutions 
            y_num = np.concatenate((y_num, np.array([yn])))
            x_num = np.append(x_num, xn)

        # Adjust the stepsize
        h *= 0.8*(tol/error_estimate)**(1/(p+1))

        
        if ncall > Maxcall:
            print("max iterations reached")
            break

    return x_num, y_num

def force(points, i):
    p = points[i]
    points = np.delete(points, i, axis = 0)

    epsilon = 1
    sigma = 1
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
    r2 = np.array([force(r[0], i) for i in range(r.shape[1])])

    return np.array([
        r[1],
        r2
    ])

n_particles = 5
np.random.seed(1)
init_speed = np.zeros((n_particles, 3))
init_pos = np.random.rand(n_particles, 3)*4
init = np.array([init_pos, init_speed])

c_n = [0, 1/2, 3/4, 1]
a_n = np.array([
    [0, 0, 0, 0],
    [1/2, 0, 0, 0],
    [0, 3/4, 0, 0],
    [2/9, 1/3, 4/9, 0]
    ])
b_n_1 = [2/9, 1/3, 4/9, 0]
b_n_2 = [7/24, 1/4, 1/3, 1/8]
rkp = RungeKutta_pair(c_n, a_n, b_n_1, b_n_2, 3, is_explicit=True)
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