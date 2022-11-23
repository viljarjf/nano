

from numpy import *
from matplotlib.pyplot import *
newparams = {'figure.figsize': (8.0, 4.0), 'axes.grid': True,
             'lines.markersize': 8, 'lines.linewidth': 2,
             'font.size': 14}
rcParams.update(newparams)
def simpson(f, a, b, m=10):
# Find an approximation to an integral by the composite Simpson's method:
# Input:
#   f:    integrand
#   a, b: integration interval
#   2*m:  number of subintervals
# Output: The approximation to the integral
    n = 2*m
    x_noder = linspace(a, b, n+1)       # equidistributed nodes from a to b
    h = (b-a)/n                         # stepsize
    S1 = f(x_noder[0]) + f(x_noder[n])  # S1 = f(x_0)+f(x_n)
    S2 = sum(f(x_noder[1:n:2]))         # S2 = f(x_1)+f(x_3)+...+f(x_m)
    S3 = sum(f(x_noder[2:n-1:2]))       # S3 = f(x_2)+f(x_4)+...+f(x_{m-1})
    S = h*(S1 + 4*S2 + 2*S3)/3
    return S
# Numerical experiment 1
def fs(x):                   # Integrand
    return 4/(1+x**2)
def newton(f, df, x0, tol=1.e-8, max_iter=30):
    # Solve f(x)=0 by Newtons method
    # The output of each iteration is printed
    # Input:
    #   f, df:   The function f and its derivate f'.
    #   x0:  Initial values
    #   tol: The tolerance
    # Output:
    #   The root and the number of iterations
    x = x0
    print('k ={:3d}, x = {:18.15f}, f(x) = {:10.3e}'.format(0, x, f(x)))
    for k in range(max_iter):
        fx = f(x)
        if abs(fx) < tol:           # Accept the solution
            break
        x = x - fx/df(x)            # Newton-iteration
        print('k ={:3d}, x = {:18.15f}, f(x) = {:10.3e}'.format(k+1, x, f(x)))
    return x, k+1
# Example 2
def f(x):                   # The function f
    return 5*x**3+5+sinh(2*x)

def df(x):                  # The derivative f'
    return 15*x**2+2*cosh(2*x)

x0 = 0                  # Starting value
x, nit = newton(f, df, x0, tol=1.e-20, max_iter=30)  # Apply Newton
print('\n\nResult:\nx={}, number of iterations={}'.format(x, nit))
a, b = 0,1              # Integration interval
S = simpson(fs, a, b, m=3)-3.14159265   # Numerical solution, using 2m subintervals
print('S = {:.8f}'.format(S))
print(f(f(f(x0))))
