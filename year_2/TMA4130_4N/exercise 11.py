import numpy as np 
import matplotlib.pyplot as plt

def runge_kutta(f, x: float, y: np.array, h: float)-> [float, np.array]:
    k1 = f(x, y)
    k2 = f(x + h/2, y + h/2*k1)
    k3 = f(x + h/2, y + h/2*k2)
    k4 = f(x + h, y + h*k3)
    return x + h, y + h/6*(k1 + 2*k2 + 2*k3 + k4)

def euler(f, x, y, h):
    return x+h, y + h*f(x, y)

def heun(f, x, y, h):
    k1 = f(x, y)
    k2 = f(x+h, y+h*k1)
    return x+h, y+h/2*(k1+k2)

def f_1(x, y):
    return -2*x*y

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


# The exact solution, for verification
def y_exact(x):
    return np.exp(-x**2)

def plot(f, x0, xend, y0, h, method, desc = ""):
    # Solve the equation
    x_num, y_num = ode_solver(f, x0, xend, y0, h, method)
    
    shape = None
    if len(x_num) <= 100:
        shape = ".-"

    if len(y_num.shape) == 2:
        if shape:
            plt.plot(x_num, y_num[:, 0], shape)
        else:
            plt.plot(x_num, y_num[:, 0])
        y_num = y_num[:, 2]
    # Plot of the exact solution
    #x = np.linspace(x0, xend, 101)
    #plt.plot(x, y_exact(x))

    # Plot of the numerical solution
    if shape:
        plt.plot(x_num, y_num, shape)
    else:
        plt.plot(x_num, y_num)

    plt.xlabel('x')
    plt.ylabel('y(x)')
    plt.legend(['u(x)', 'v(x)'])
    plt.title(desc)
    plt.show()

def errors(f, x0, xend, y0, h, method):
    print("h           error       relative error")
    prev_error = 1
    for n in range(10):
        x_num, y_num = ode_solver(f, x0, xend, y0, h, runge_kutta)   # Solve the equation 
        error = abs(y_exact(xend)-y_num[-1])            # Error at the end point
        print(format('{:.3e}   {:.3e}   {:.3e}'.format( h, error, error/prev_error)))   
        h *= 0.5
        prev_error = error

def f_2(x, y):
    a = y[1]
    b = 1/10*(-100*y[0] + 200*(y[2] - y[0]))
    c = y[3]
    d = 1/5*(-200*(y[2]-y[0]))
    return np.array([a, b, c, d])

def E(y):
    return 0.5*(10*y[1]**2 + 5*y[3]**2 + 100*y[0]**2 + 200*(y[0]-y[2])**2)

def plot_E(f, x0, xend, y0, h, method, desc = ""):
    # Solve the equation
    x_num, y_num = ode_solver(f, x0, xend, y0, h, method)
    
    shape = None
    if len(x_num) <= 100:
        shape = ".-"

    # Plot of the numerical solution
    if shape:
        plt.plot(x_num, E(y_num.transpose()), shape)
    else:
        plt.plot(x_num, E(y_num.transpose()))

    plt.xlabel('x')
    plt.ylabel('y(x)')
    plt.legend(['u(x)', 'v(x)'])
    plt.title(desc)
    plt.show()

if __name__ == "__main__":
    
    print("Task 1 b)")
    errors(f_1, 0, 1, 1, 0.5, runge_kutta)
    """
    result:
    h           error       relative error
    5.000e-01   1.524e-04   1.524e-04
    2.500e-01   5.505e-05   3.613e-01
    1.250e-01   3.927e-06   7.133e-02
    6.250e-02   2.501e-07   6.368e-02
    3.125e-02   1.565e-08   6.257e-02
    1.562e-02   9.768e-10   6.243e-02
    7.812e-03   6.099e-11   6.244e-02
    3.906e-03   3.809e-12   6.246e-02
    1.953e-03   2.381e-13   6.252e-02
    9.766e-04   1.449e-14   6.084e-02

    The relative error converges towards 1/8, which is 1/2**3 as expected for p = 3
    """
    
    print("\n\n", heun(f_2, 0, np.array([0,1,0,1]), 0.1))
    print("\n\nTask 3 c)")
    plot(f_2, 0, 3, np.array([0,1,0,1]), 0.1, heun, "Heun, h=0.1")
    plot(f_2, 0, 3, np.array([0,1,0,1]), 0.01, heun, "Heun, h=0.01")
    plot(f_2, 0, 3, np.array([0,1,0,1]), 0.001, heun, "Heun, h=0.001")
    plot(f_2, 0, 3, np.array([0,1,0,1]), 0.1, euler, "euler, h=0.1")
    plot(f_2, 0, 3, np.array([0,1,0,1]), 0.01, euler, "euler, h=0.01")
    plot(f_2, 0, 3, np.array([0,1,0,1]), 0.001, euler, "euler, h=0.001")
    # Both are sinusoidal, but heun converges quicker

    print("\n\nTask 3 d")
    plot_E(f_2, 0, 3, np.array([0,1,0,1]), 0.1, heun, "Energy, Heun, h=0.1")
    plot_E(f_2, 0, 3, np.array([0,1,0,1]), 0.01, heun, "Energy, Heun, h=0.01")
    plot_E(f_2, 0, 3, np.array([0,1,0,1]), 0.001, heun, "Energy, Heun, h=0.001")
    plot_E(f_2, 0, 3, np.array([0,1,0,1]), 0.1, euler, "Energy, euler, h=0.1")
    plot_E(f_2, 0, 3, np.array([0,1,0,1]), 0.01, euler, "Energy, euler, h=0.01")
    plot_E(f_2, 0, 3, np.array([0,1,0,1]), 0.001, euler, "Energy, euler, h=0.001")
    # although the energy seems to increase linearly, it increases very slowly. 