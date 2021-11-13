from typing import Callable
from scipy.special import erf
from scipy import integrate, optimize
import numpy as np
import numpy.ma as ma
from matplotlib import pyplot as plt
import os
from PIL import Image


METERS_PER_PIXEL = (500*10**-6) / 210.5
a = 3/4*(75*500)*10**-12
q = 8/3*10**-9
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
            grayscale[i, j] = normalize(arr[i, j])
        
    masked = ma.array(grayscale, mask = arr[:, : , -1] < 100)
    #Image.fromarray(masked*255).show()
    
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
    y = y_j(j+1)
    sqrt = lambda x: x**0.5
    pi = np.pi
    A = A_ij(i,j)
    factor = y / sqrt(x) #-8*a*q*x*y / (sqrt(pi) *sqrt(q / (D *a *x))* (4*D *a *x)**2)
    exponent = np.exp(-(1 / 2 *y *sqrt(q / (D *a* x)))**2)
    error = -1 / 2* (-erf(1 / 2 *y *sqrt(q / (D *a *x))) + 1) + A
    return factor*exponent*error


def eq11(D: float, x: int = None) -> float:
    """Sum over i and j"""
    if x is None:
        x = range(DATA_SHAPE[1])
    res = 0
    for j in range(DATA_SHAPE[0]):
        for i in x:#
            if A_ij(i,j) == ma.masked:
                continue
            res += eq_11_ij(D, i, j)
    return res


def est_ij(D, i, j):
    """Calculate A based on the actual equation"""
    arg = y_cont(j + 1)*(q / (4*D*a*x_cont(i)))**0.5
    e = 1 - erf(arg)
    return 0.5*(e)


def d_eq11(D: float, i) -> float:
    """Numerical derivation"""
    dD = 10**-17
    return (eq11(D+dD, i) - eq11(D, i))/dD


def D_next(D_n, i):
    """Newton's method"""
    return D_n - eq11(D_n, i) / d_eq11(D_n, i)


def get_D(D_0: float = None, rel_error: float = None, i = None) -> float:
    """Calculate D with Newton's method"""
    if D_0 is None:
        D_0 = 6.1*10**-8
    if rel_error is None:
        rel_error = 10**-4
    Dn = D_next(D_0, i)
    D = D_0
    n = 0
    while abs(1 - Dn / D) > rel_error:
        e = abs(1-D/Dn)
        print(f"{n} & {D :.4g} & {e :.4g} \\\\")
        n += 1
        D, Dn = D_next(Dn, i), D
    e = abs(1-D/Dn)
    print(f"{n} & {D :.4g} & {e :.4g} \\\\")
    return D


def find_error(real: list[int], model: Callable[[float], float]) -> float:
    """integrate the square difference"""
    def real_func(y):
        j = -y/METERS_PER_PIXEL + 1 + MAX_Y/2
        j_int = int(j)
        j_float = j - j_int
        return (real[j_int] - real[j_int - 1]) * j_float + real[j_int - 1]

    return integrate.quad(lambda y: (real_func(y) - model(y))**2, y_j(MAX_Y), y_j(0))


def main():
    """
    D = []
    for i in range(100, DATA_SHAPE[1]):
        if i < 100:
            s = 10**-6
        else:
            s = 10**-9
        D.append(get_D(s, i = [i]))
        print(D[-1])
    D = np.array(D)

    print(np.count_nonzero(np.isnan(D)))
    print(np.mean(D[~np.isnan(D)]))
    print(np.std(D[~np.isnan(D)]))
    #"""
    D = get_D(10**-9)
    r = 2.08 * 10**-19 / D
    print(f"{D = :.2g}, {r = :.2g}")
    """
    x = np.logspace(-11, -9, 1000, base = 10)
    y = eq11(x)
    plt.plot(10**12*x, y)
    plt.xlabel("D ($\\frac{µm^2}{s}$)")
    plt.ylabel("f(D)")
    plt.xscale("log")
    plt.title("Plot of equation 11")
    plt.show()
    #"""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2)
    x1, x2, x3, x4 = 20, 200, 500, 900
    y = [i for i in range(MAX_Y)]
    y_plot = [y_j(j) for j in y]
    y_c = np.linspace(0, MAX_Y, 1000)
    y_plot_c = y_cont(y_c)
    

    ax1.scatter(y_plot, [A_ij(x1, j) for j in y], s = 4)
    ax1.plot(y_plot_c, est_ij(D, x1, y_c), "m")
    ax1.set_title(f"A: x = {round(x_i(20)*10**6)}µm (20 px)")
    ax1.set_xlabel("y (m)")
    ax1.set_ylabel("Intensity")
    #I, e = find_error([A_ij(x1, j) for j in y], lambda y: est_ij(D, x1, y))
    ax1.text(x = y_j(40), y = 0.5, s = f"D: 2.8·10³ \nµm² / s")

    ax2.scatter(y_plot, [A_ij(x2, j) for j in y], s = 4)
    ax2.plot(y_plot_c, est_ij(D, x2, y_c), "m")
    ax2.set_title(f"B: x = {round(x_i(200)*10**6)}µm (200 px)")
    ax2.set_xlabel("y (m)")
    ax2.set_ylabel("Intensity")
    #I, e = find_error([A_ij(x2, j) for j in y], lambda y: est_ij(D, x2, y))
    ax2.text(x = y_j(40), y = 0.5, s = f"D: 0.55·10³ \nµm² / s")
    
    ax3.scatter(y_plot, [A_ij(x3, j) for j in y], s = 4)
    ax3.plot(y_plot_c, est_ij(D, x3, y_c), "m")
    ax3.set_title(f"C: x = {round(x_i(500)*10**6)}µm (500 px)")
    ax3.set_xlabel("y (m)")
    ax3.set_ylabel("Intensity")
    #I, e = find_error([A_ij(x3, j) for j in y], lambda y: est_ij(D, x3, y))
    ax3.text(x = y_j(40), y = 0.5, s = f"D: 1.1·10³ \nµm² / s")

    ax4.scatter(y_plot, [A_ij(x4, j) for j in y], s = 4)
    ax4.plot(y_plot_c, est_ij(D, x4, y_c), "m")
    ax4.set_title(f"D: x = {round(x_i(900)*10**6)}µm (900 px)")
    ax4.set_xlabel("y (m)")
    ax4.set_ylabel("Intensity")
    #I, e = find_error([A_ij(x4, j) for j in y], lambda y: est_ij(D, x4, y))
    ax4.text(x = y_j(40), y = 0.5, s = f"D: 0.36·10³ \nµm² / s")

    plt.legend(["Model", "Data"])
    fig.suptitle("Comparing model values to data at different points along the channel")
    plt.show()
    
if __name__ == "__main__":
    main()