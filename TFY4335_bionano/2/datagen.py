from typing import Any, Callable
from matplotlib import pyplot as plt
import os
import numpy as np

FIGURE_DIR = os.path.join(os.path.dirname(__file__), "figs")
DRAW_STEPS = 1000
D = 10**(-11)

def plot(
    f: Callable[[np.ndarray], np.ndarray], 
    x0: float,
    xn: float,
    f_args: tuple = None,
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

    if f_args is None:
        y = f(x)
    else:
        y = f(x, *f_args)

    testx = (xn + x0)/2
    testval = f(testx, *f_args)
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
    

def c(x, t):
    return np.power(4*np.pi*D*t, -0.5) * np.exp(-np.power(x, 2)/(4*D*t))

def main():
    x0 = -10**-6
    xn = 10**-6
    plot(c, x0, xn, f_args = (0.001,), clear = False)
    plot(c, x0, xn, f_args = (0.01,), clear = False)
    legend = [
        "C(x, 0.001)",
        "C(x, 0.01)",
        "C(x, 0.1)",
    ]
    plot(
        c, 
        x0, 
        xn, 
        f_args = (0.1,),
        title = "Concentration profiles",
        x_label = "x (m)",
        y_label = "Concentration (units of $c_0$)",
        legend = legend, 
        save = True
    )



if __name__ == "__main__":
    main()