from typing import Any, Callable
from matplotlib import pyplot as plt
import os
import numpy as np

FIGURE_DIR = os.path.join(os.path.dirname(__file__), "figs")
DRAW_STEPS = 1000

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
    rho = 2.17 * 10**6 # g/m^3
    v = 1 / rho
    return (v / a**3)

def surface_energy(a: float | np.ndarray) -> float | np.ndarray:
    gamma = 0.2
    return 6 * gamma * a**2 * n_cubes(a)

def edge_energy(a: float | np.ndarray) -> float | np.ndarray:
    sigma = 3*10**(-11)
    return 12 * sigma * a * n_cubes(a)

def surface_and_edge_energy(a: float | np.ndarray) -> float | np.ndarray:
    return surface_energy(a) + edge_energy(a)

def fusion_enthalpy(a: Any) -> np.ndarray:
    std = 27950
    Mm = 58.44
    return np.ones(DRAW_STEPS) * std / Mm

def sphere_surface_to_bulk_ratio(r: float | np.ndarray) -> float | np.ndarray:
    r_pd = 1.37*10**-10
    rho = 12 * 10**6 # g/m^3
    Mm = 106.4
    mol = 6.022 * 10**23

    vol = 4/3*np.pi*r**3
    mass = vol * rho # g
    n_atoms = np.rint(mass / Mm * mol)

    area = 4*np.pi*r**2
    s_atoms = np.rint(area / (4*r_pd**2))

    return s_atoms / (n_atoms - s_atoms)

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

    plot(
        sphere_surface_to_bulk_ratio,
        x0,
        xn,
        "Ratio of surface and bulk atoms",
        xscale = "log",
        x_label = "Nanoparticle radius (m)",
        y_label = "Ratio of surface particles to bulk particles",
        save = True,
    )


if __name__ == "__main__":
    main()