import matplotlib.pyplot as plt
from scipy import special
import numpy as np
from scipy.optimize.minpack import curve_fit
from functools import cache

@cache
def lag(a,b):
    if b == 0:
        return 1
    if b == a-1:
        return 1
    if b >= a:
        return 0

    if b <= a/2:
        return sum(lag(b,n) for n in range(b))
    return sum(lag(b,b-n) for n in range(1, a-b+1))

def mult(n):
    return sum(lag(n,i) for i in range(n))

def gamma(x, k, th):
    return x**(k-1) / (special.gamma(k)*th**k)*np.exp(-x/th)

def planc(x, T, a, b):
    return 2*x**3 *a /(np.exp(b*x/T) - 1)

def chi(x, k):
    return x**(k/2 -1)*np.exp(-x/2)/(2**(k/2)*special.gamma(k/2))

def gumbel(x, a, b):
    return a*b*np.exp(-a*x - b*np.exp(-a*x))

def gumbel2(x, a, b):
    return a*b*x**(-a-1)*np.exp(-b-x**-a)

N = 10000
print((3/(2*N))**0.5*np.log(np.array([mult(N)]).astype(np.float64)))
#x = [i for i in range(1, 1000)]
#y = np.array([mult(i) for i in x]).astype(np.float64)
#y = np.log(y)

#plt.plot(x,y)
#plt.show()
"""
a = [0.5]
b = [8]
x = []
for N in range(10, 601):
    _x = [x for x in range(1,N)]
    y = [lag(N,i) for i in _x][::-1]
    s = sum(y)
    y_norm = [i/s for i in y]

    r = curve_fit(gumbel, _x, y_norm, np.array([a[-1], b[-1]]))
    _a,_b = r[0]
    a.append(_a)
    b.append(_b)
    x.append(N)

a = a[1:]
b = b[1:]


#r = curve_fit(gumbel2, x, y_norm, np.array([3, 4]))
#print(r)
#a,b = r[0]
#f = lambda x: a*b*x**(-a-1)*np.exp(-b-x**-a)

f = lambda x: _a*_b*np.exp(-_a*x - _b*np.exp(-_a*x))

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)

ax1.plot(_x,y_norm)
ax1.plot(_x, [f(i) for i in _x])
ax1.legend(["Normalised actual distribution", "Curve-fit of type-1 Gumbel distribution"])
ax1.set_title(f"Degeneracy of states for E={N}")
ax1.set(xlabel = "Highest-energy particle for a state", ylabel = "Relative frequency")


ax2.plot(_x, [j - f(i) for i,j in zip(_x,y_norm)])
ax2.set_title(f"Error in curve-fit for U={N}")
ax2.set(xlabel = "Highest-energy particle for a state", ylabel = "Error")


ax3.plot(x,a)
ax3.set_title("a-parameter of the Gumbel distribution as a function of U")
ax3.set(xlabel = "U", ylabel = "a")

ax4.plot(x,b)
ax4.set_title("b-parameter of the Gumbel distribution as a function of U")
ax4.set(xlabel = "U", ylabel = "b")

plt.show()
"""