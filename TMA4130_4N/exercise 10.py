import matplotlib.pyplot as plt
import numpy as np

def simpson(f, a, b, m=10):
    """
    Find an approximation to an integral by the composite Simpson's method:
    Input:
        f:    integrand
        a, b: integration interval
        m:    number of subintervals
    Output: 
        The approximation to the integral
    """
    n = 2*m
    x_noder = np.linspace(a, b, n+1)        # equidistributed nodes from a to b
    h = (b-a)/n                             # stepsize
    S1 = f(x_noder[0]) + f(x_noder[n])      # S1 = f(x_0)+f(x_n)
    S2 = sum(f(x_noder[1:n:2]))             # S2 = f(x_1)+f(x_3)+...+f(x_m)
    S3 = sum(f(x_noder[2:n-1:2]))           # S3 = f(x_2)+f(x_4)+...+f(x_{m-1})
    S = h*(S1 + 4*S2 + 2*S3)/3
    return S

def f_task_1(x):
    return np.exp(-x)

def task_2(f, a, b, exact):
    # Find an numerical approximation for different values of h. 
    # Store the stepsize h and the error
    n = 1                           # initial stepsize, h=(b-a) 
    h = (b-a)/(2*n)
    steps = []                      # arrays to store stepsizes and errors
    errors = []
    Nmax = 10
    for k in range(Nmax):
        numres = simpson(f, a, b, n)    # Numerical approximation
        eh = abs(exact - numres)            # Error e(h)
        steps.append(h)                     # Append the step to the array
        errors.append(eh)                   # Append the error to the array
        n = 2*n                             # Reduce the stepsize with a factor 2
        h = (b-a)/(2*n)

    # Find the order and the error constant
    print('\nThe order p and the error constant C')
    for k in range(1, Nmax-1):
        p = np.log(errors[k+1]/errors[k])/np.log(steps[k+1]/steps[k])
        C = errors[k+1]/steps[k+1]**p
        print('h = {:8.2e},  p = {:4.2f},  C = {:6.4f}'.format(steps[k], p, C))

    # Make an error plot
    plt.clf()
    plt.loglog(steps, errors, 'o-')
    plt.xlabel('h')
    plt.ylabel('e(h)')
    plt.title("Error plot for Simpson's rule")
    plt.grid('True')
    plt.show()

def f_task_2_a(x):
    return x*np.exp(x)

def f_task_2_b(x):
    return (1-x**2)**0.5*np.exp(x)

def gauss(f, a, b):
    x0 = -(3/5)**0.5
    x1 = 0
    x2 = -x0

    c = (b+a)/2
    h = (b-a)/2

    w0 = 5/9
    w1 = 8/9
    w2 = w0

    return h * (w0*f(h*x0 + c) + w1*f(h*x1 + c) + w2*f(h*x2 + c))

def gauss_basic(f, a, b):
    """
     Input:
       f:    integrand
       a, b: integration interval
     Output:  Q_2(a,b) and the error estimate.
    """

    c = 0.5*(a+b)
    # Calculate S1=S_1(a,b), S2=S_2(a,b)
    Q1 = gauss(f, a, b)
    Q2 = gauss(f, a, c) + gauss(f, c, b)
    error_estimate = (Q2-Q1)/63 # Error estimate for Q2
    return Q2, error_estimate


def f_task_3_f(x):
    return np.exp(-x)

if __name__ == "__main__":

    print("Task 1 c")
    val = simpson(f_task_1, 1, 3, m=26)
    print("Numeric value:", val, "\nError:", np.exp(-1)-np.exp(-3)-val)
    # Output: 
    """
    Numeric value: 0.31809237667001494
    Error: -3.86643655980734e-09
    """

    print("\n\nTask 2 a")
    task_2(f_task_2_a, -1, 1, 2/np.e)
    # Output: 
    """ 
    The order p and the error constant C
    h = 5.00e-01,  p = 3.95,  C = 0.0522
    h = 2.50e-01,  p = 3.99,  C = 0.0548
    h = 1.25e-01,  p = 4.00,  C = 0.0558
    h = 6.25e-02,  p = 4.00,  C = 0.0562
    h = 3.12e-02,  p = 4.00,  C = 0.0563
    h = 1.56e-02,  p = 4.00,  C = 0.0563
    h = 7.81e-03,  p = 4.00,  C = 0.0563
    h = 3.91e-03,  p = 4.00,  C = 0.0562
    """

    print("\n\nTask 2 b")
    task_2(f_task_2_b, -1, 1, 1.7754996892121809469)
    # Output:
    """
    The order p and the error constant C
    h = 5.00e-01,  p = 1.59,  C = 0.4208
    h = 2.50e-01,  p = 1.54,  C = 0.3943
    h = 1.25e-01,  p = 1.52,  C = 0.3769
    h = 6.25e-02,  p = 1.51,  C = 0.3670
    h = 3.12e-02,  p = 1.50,  C = 0.3614
    h = 1.56e-02,  p = 1.50,  C = 0.3583
    h = 7.81e-03,  p = 1.50,  C = 0.3565
    h = 3.91e-03,  p = 1.50,  C = 0.3556
    """

    print("\n\nTask 3 f")
    x5 = lambda x: x**5
    x6 = lambda x: x**6
    print("x^5: ", gauss_basic(x5, -1, 1))
    print("x^6: ", gauss_basic(x6, -1, 1))
    print("e^-x:", gauss_basic(f_task_3_f, 1, 3))
    print("Exact error / estimated error: ", (np.exp(-1) - np.exp(-3) - gauss_basic(f_task_3_f, 1, 3)[0]) / gauss_basic(f_task_3_f, 1, 3)[1])
    # Output:
    """
    x^5:  (0.0, 0.0)
    x^6:  (0.28500000000000003, 0.0007142857142857136)
    e^-x: (0.3180922202467432, 1.3819527561099315e-07)
    Exact error / estimated error:  1.1039222179635708
    """
    # the last line shows that the error estimate is ~10% off
