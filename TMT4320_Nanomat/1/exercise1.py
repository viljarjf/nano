from typing import Any, Callable
from matplotlib import pyplot as plt
import os
import numpy as np

FIGURE_DIR = os.path.join(os.path.dirname(__file__), "figs")
DRAW_STEPS = 1000
RHO_NACL = 2.17 * 10**6 # g/m^3
GAMMA = 0.2
SIGMA = 3*10**(-11)
STD_ENTAHLPY_NACL = 27950
MM_NACL = 58.44
R_PD = 1.37*10**-10
RHO_PD = 12 * 10**6 # g/m^3
MM_PD = 106.4
MOL = 6.022 * 10**23

def plot(
    f: Callable[[np.ndarray], np.ndarray], 
    x0: float,
    xn: float,
    title: str = None,
    x_label: str = None,
    y_label: str = None,
    xscale: str = None,
    yscale: str = None,
    save: bool = False,
    clear: bool = True,
    legend: list[str] = None
    ) -> None:

    if xscale == "log":
        x = np.logspace(np.log(x0), np.log(xn), DRAW_STEPS, base = np.e)
    else:
        x = np.linspace(x0, xn, DRAW_STEPS)
    y = f(x)

    plt.plot(x, y)

    if title is not None:
        plt.title(title)
    if x_label is not None:
        plt.xlabel(x_label)
    if y_label is not None:
        plt.ylabel(y_label)
    if legend is not None:
        plt.legend(legend)
    if yscale  is not None:
        plt.yscale(yscale)
    if xscale is not None:
        plt.xscale(xscale)
    if save:
        if title is None:
            raise ValueError("Cannot save without a defined title")
        filepath = os.path.join(FIGURE_DIR, title.replace(" ", "_") + ".png")
        plt.savefig(filepath)
    if clear:
        plt.clf()


def n_cubes(a: float | np.ndarray) -> float | np.ndarray:
    v = 1 / RHO_NACL
    return (v / a**3)

def surface_energy(a: float | np.ndarray) -> float | np.ndarray:
    return 6 * GAMMA * a**2 * n_cubes(a)

def edge_energy(a: float | np.ndarray) -> float | np.ndarray:
    return 12 * SIGMA * a * n_cubes(a)

def surface_and_edge_energy(a: float | np.ndarray) -> float | np.ndarray:
    return surface_energy(a) + edge_energy(a)

def fusion_enthalpy(a: Any) -> np.ndarray:

    return np.ones(DRAW_STEPS) * STD_ENTAHLPY_NACL / MM_NACL

def sphere_surface_to_bulk_ratio(r: float | np.ndarray) -> float | np.ndarray:
    vol = 4/3*np.pi*r**3
    mass = vol * RHO_PD # g
    n_atoms = np.rint(mass / MM_PD * MOL)

    area = 4*np.pi*r**2
    s_atoms = np.rint(area / (4*R_PD**2))

    return s_atoms / (n_atoms - s_atoms)

def add_sphere_surface_to_bulk_ratio_discrete():
    # hard coding :((
    shells = np.array([1, 2, 3, 4, 5, 7])
    r = R_PD*(shells*2 + 1)

    ratio = np.array([0.92, 0.76, 0.63, 0.52, 0.45, 0.35])
    plt.scatter(r, ratio / (1-ratio))

def r_to_n(r: float | np.ndarray) -> float | np.ndarray:
    return r/(2*R_PD) - 0.5

def exact_ratio(r: float | np.ndarray) -> float | np.ndarray:
    n = r_to_n(r)
    return (30*n**2 + 6)/(10*n**3 -15*n**2 + 11*n -3)

def main():
    x0 = 10**-9
    xn = 10**-7
    plot(surface_energy, x0, xn, xscale = "log", clear = False)
    plot(edge_energy, x0, xn, xscale = "log", clear = False)
    plot(fusion_enthalpy, x0, xn, xscale = "log", clear = False)
    legend = [
        "Surface energy",
        "Edge energy",
        "Fusion enthalpy",
        "Total energy"
    ]
    plot(
        surface_and_edge_energy, 
        x0, 
        xn, 
        title = "Energy of 1g NaCl as a function of cube size",
        x_label = "Cube side length (m)",
        y_label = "Energy (J)",
        xscale = "log", 
        #yscale = "log",
        legend = legend, 
        save = True
    )

    x0 = 3*R_PD
    xn = 10**-8
    add_sphere_surface_to_bulk_ratio_discrete()
    plot(exact_ratio, x0, xn, xscale = "log", clear = False)
    x0 = 6.5*10**-10
    plot(
        sphere_surface_to_bulk_ratio,
        x0,
        xn,
        "Ratio of surface and bulk atoms",
        xscale = "log",
        x_label = "Nanoparticle radius (m)",
        y_label = "Ratio of surface particles to bulk particles",
        save = True,
        legend = [
            "Exact",
            "Model",
            "Measured values"
        ]
    )


if __name__ == "__main__":
    main()