import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve


class RK:
    def __init__(self, c, a, b, p=0):
        self.a = np.array(a)
        self.c = np.array(c)
        self.b = np.array(b)
        self.p = p
        self.prev_k = None

    def __call__(self, f, xn, yn, h):
        k_shape = (len(self.c), len(yn))
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
        if self.prev_k is None:
            k = np.array(fsolve(func, np.ones(k_shape))).reshape(k_shape)
        else:
            k = np.array(fsolve(func, self.prev_k)).reshape(k_shape)
        self.prev_k = k
        if len(k) == 1:
            add = self.b[0]*k[0]
        else:
            add = np.sum([self.b[j]*k[j] for j in range(len(k))], axis = 0)
        y_next = yn + h*add
        x_next = xn + h
        return x_next, y_next

class RK_pair:
    def __init__(self, c, a, b_1, b_2, p):
        self.rk2 = RK(c, a, b_2)
        self.b1 = b_1
        self.b2 = b_2
        self.p = p

    def __call__(self, f, xn, yn, h):
        x_next, y_next = self.rk2(f, xn, yn, h)
        error_estimate = h*np.sum([(self.b2[i]-self.b1[i])*self.rk2.prev_k[i] for i in range(len(self.rk2.prev_k))], axis = 0)
        error_estimate = np.linalg.norm(error_estimate)
        return x_next, y_next, error_estimate, self.p

def lotka_volterra(x, y):
    alpha, beta, delta, gamma = 2, 1, 0.5, 1     # Set the parameters
    dy = np.array([alpha*y[0]-beta*y[0]*y[1],       
                delta*y[0]*y[1]-gamma*y[1]])
    return dy


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
    yn = y0 

    # Main loop
    while xn < xend - 1.e-10:            # Buffer for truncation errors        
        xn, yn = method(f, xn, yn, h)    # Do one step by the method of choice
        
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
    yn = y0 
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

        
        # Stop with a warning in the case of max calls to method
        if ncall > Maxcall:
            print('Maximum number of method calls')
            return x_num, y_num

    # Some diagnostic output
    print('Number of accepted steps = ', len(x_num)-1)
    print('Number of rejected steps = ', ncall - len(x_num)+1)
    return x_num, y_num

euler = RK([0], [np.array([0])], [1])
heun = RK([0, 1], [[0,0], [1,0]], [0.5, 0.5])

c = [0, 1/2, 3/4, 1]
a = np.array([[0, 0, 0, 0], 
     [0.5, 0, 0, 0],
     [0, 0.75, 0, 0],
     [2/9, 1/3, 4/9, 0]])
b_1 = [2/9, 1/3, 4/9, 0]
b_2 = [7/24, 1/4, 1/3, 1/8]

c_n = [0, 1/2, 1]
a_n = np.array([[1/6, -1/3, 1/6],
        [1/6, 5/12, -1/12],
        [1/6, 2/3, 1/6]])
b_n_1 = [1/6, 2/3, 1/6]
b_n_2 = [-1/2, 2, -1/2]

def henrik(x, y):
    sigma, rho, beta = 2, 0.5, 2/3
    return np.array([sigma*(y[1]-y[0]), y[0]*(rho - y[2]) - y[1], y[0]*y[1] - beta*y[2]])

import time
start = time.time()
rkp = RK_pair(c_n, a_n, b_n_1, b_n_2, 4)
x, y = adaptive(henrik, 0, 5, [2, 0.5, 1], 0.01, rkp, tol = 1.e-6)
print("Took", time.time()-start, "seconds")
#rk5 = RK(c, a, b_2)
#x, y = ode_solver(lotka_volterra, 0, 20, [2, 0.5], 0.01, rk5)

plt.plot(x, y[:, 0])
plt.plot(x, y[:, 1])
plt.plot(x, y[:, 2])
plt.legend(["x", "y", "z"])
plt.show()
