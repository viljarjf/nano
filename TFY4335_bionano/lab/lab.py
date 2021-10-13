from scipy.special import erf
import numpy as np
import numpy.ma as ma
from matplotlib import pyplot as plt
import os
from PIL import Image

METERS_PER_PIXEL = (75*10**-6) / 210.5
a = (75*10**-6)**2
q = 5/3*10**-11
DATA_SHAPE = (40, 929)
MAX_Y = 40
MAX_X = 929

def get_data() -> np.ndarray:
    """Open the image file, convert to grayscale, normalize and return the arr"""
    img = Image.open(os.path.join(os.path.dirname(__file__), "crop_micro_output_4x_80µl.png"))
    arr = np.asarray(img)
    #img.show()

    def linearize(C):
        C /= 255
        return C/12.92 if C  <= 0.04045 else ((C + 0.055) / 1.055)**2.4

    def normalize(rgb):
        Y = 0.2126 * linearize(rgb[0])
        Y += 0.7152 * linearize(rgb[1])
        Y += 0.0722 * linearize(rgb[2])
        return Y

    grayscale = np.zeros(arr.shape[:-1], dtype = np.float32)
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            v = normalize(arr[i, j])
            grayscale[i, j] = v
        
    masked = ma.array(grayscale, mask = arr[:, : , -1] < 100)
    #Image.fromarray(masked*255).show()
    for j in range(arr.shape[1]):
        tmp = (masked[:, j] - np.mean(masked[:15, j]))
        masked[:, j] = tmp/np.mean(tmp[-15:])
        
    masked = np.fliplr(masked)
    #Image.fromarray(masked*255).show()
    return masked

def x_i(i: int) -> float:
    return (i+1)*METERS_PER_PIXEL

def x_cont(i: float) -> float:
    return (i+1)*METERS_PER_PIXEL

def y_j(j: int) -> float:
    return (MAX_Y/2 - j+1 ) *METERS_PER_PIXEL
    
def y_cont(j: float) -> float:
    return (MAX_Y/2 - j+1 )*METERS_PER_PIXEL

def A_ij(i: int, j: int, A: ma.MaskedArray = get_data()) -> float:
    return A[j,i]

def eq_11_ij(D: float, i: int, j: int) -> float:
    """Calculate each element in the sum"""
    x = x_i(i)
    y = y_j(j)
    sqrt = lambda x: x**0.5
    pi = np.pi
    A = A_ij(i,j)
    factor = -0.5*a*q*x*y/(sqrt(pi)*(D*q*x)**2*sqrt(a/(D*q*x)))
    exponent = np.exp(-(0.5*y*(a/(D*q*x))**0.5)**2)
    error = -0.5*(-erf(0.5*y*sqrt(a/(D*q*x))) + 1) + A
    return factor*exponent*error

def eq11(D: float) -> float:
    """Sum over i and j"""
    res = 0
    for j in range(DATA_SHAPE[0]):
        for i in range(DATA_SHAPE[1]):
            if A_ij(i,j) == ma.masked:
                continue
            res += eq_11_ij(D, i, j)
    return res

def est(D, i, j):
    """Calculate A based on the actual equation"""
    arg = y_cont(j)*(a / (4*D*q*x_cont(i)))**0.5
    e = 1 - erf(arg)
    return 0.5*(e)

def d_eq11(D: float) -> float:
    """Numerical derivation"""
    dD = 10**-17
    return (eq11(D+dD) - eq11(D))/dD

def D_next(D_n):
    """Newton's method"""
    return D_n - eq11(D_n) / d_eq11(D_n)

def get_D(D_0: float = None, rel_error: float = None) -> float:
    """Calculate D with Newton's method"""
    if D_0 is None:
        D_0 = 3.8320790839993787*10**-7
    if rel_error is None:
        rel_error = 10**-4
    Dn = D_next(D_0)
    D = D_0
    while abs(1 - Dn / D) > rel_error:
        D, Dn = D_next(Dn), D

    return D

def main():

    D = get_D()
    r = 2.08 * 10**-19 / D
    print(f"{D = :.2g}, {r = :-2g}")
    
    # 1e-16 til 1e-14: jo mindre jo bedre
    # 1e-8 til 1.1e-8: krysser ordentlig rundt 1.2
    x = np.logspace(-14, -6, 1000, base = 10)
    y = eq11(x)
    plt.plot(x, y)
    plt.xlabel("D ($\\frac{m^2}{s}$)")
    plt.ylabel("Derivative of sum of sqared errors")
    plt.xscale("log")
    plt.title("Plot of equation 11")
    plt.show()

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2)
    x1, x2, x3, x4 = 20, 200, 500, 900
    y = [i for i in range(MAX_Y)]
    y_cont = np.linspace(0, MAX_Y, 1000)

    ax1.plot(y, [A_ij(x1, j) for j in y])
    ax1.plot(y_cont, est(D, x1, y_cont))
    ax1.set_title(f"A: x = {round(x_i(20)*10**6)}µm (20 px)")

    ax2.plot(y, [A_ij(x2, j) for j in y])
    ax2.plot(y_cont, est(D, x2, y_cont))
    ax2.set_title(f"B: x = {round(x_i(200)*10**6)}µm (200 px)")
    
    ax3.plot(y, [A_ij(x3, j) for j in y])
    ax3.plot(y_cont, est(D, x3, y_cont))
    ax3.set_title(f"C: x = {round(x_i(500)*10**6)}µm (500 px)")

    ax4.plot(y, [A_ij(x4, j) for j in y])
    ax4.plot(y_cont, est(D, x4, y_cont))
    ax4.set_title(f"D: x = {round(x_i(900)*10**6)}µm (900 px)")

    plt.legend(["Data", "Model"])
    fig.suptitle("Comparing model values to data at different points along the channel")
    plt.show()
    
if __name__ == "__main__":
    main()