import matplotlib.pyplot as plt
import numpy as np

class Fourier:

    def __init__(self, f, a_n, b_n, L = None):
        """Create a function to compute the fourier transform of another function

        Args:
            f (function): the function to transform
            a (function): cosine coefficients. MUST INCLUDE n=0
            b (function): sine coefficients
        """
        self._f = f
        self._a = a_n
        self._b = b_n
        if not L:
            L = np.pi
        self._min = -L
        self._max = L
        self._L = L

    def f(self, x):
        # range-check
        s = np.sign(x)
        x = abs(x)
        x += abs(self._min)
        x %= (self._max - self._min)
        x -= abs(self._min)
        x *= s
        
        return self._f(x) 

    def fourier(self, N, x):
        if type(x) == np.ndarray:
            res = np.zeros(x.shape)
            res += self._a(0)
        else:
            res = self._a(0)
        if N >= 1:
            for m in range(1, N+1):
                res += self._a(m)*np.cos(m*x*np.pi/self._L) + self._b(m)*np.sin(m*x*np.pi/self._L)
        return res

    def plot(self, N, steps, L = None):
        if not L:
            L = self._L
        X = np.arange(-L, L, 1/steps)
        plt.plot(X, self._f(X))
        plt.plot(X, self.fourier(N, X))
        plt.show()

def a(n):
    if n == 3:
        return 1
    return 0

def b(n):
    if n == 2:
        return -0.5
    return 4/(n*np.pi) if n%2 == 1 else 0

def f(x):
    return np.cos(3*x) -0.5*np.sin(2*x) + np.sign(x)

fo = Fourier(f, a, b)
fo.plot(100, 2000)


