from spin import *

import numpy as np
from scipy import optimize 
from matplotlib import pyplot as plt

def curvefit(x: np.ndarray, dt: float) -> tuple[float, float]:
    """tau, omega"""
    def f(t, tau, omega):
        return np.cos(omega * t) * np.exp(-t/tau)
    
    t = dt*np.arange(x.size)
    (tau, omega), _ = optimize.curve_fit(f, t, x)
    return tau, omega


def run():
    print(__file__)
    c = DEFAULT_C.copy()
    c.alpha = 0.1

    iters = 1000
    additional_iters = 100

    Sj0 = np.array([[[-0.1, 0, 0.8]]])
    Sj0 = heun.normalize(Sj0)

    Sji, pad = LLG.pad(c, Sj0)
    Sjn = np.zeros((iters+1, *Sj0.shape))
    Sjn[0, ...] = Sj0

    dSj = LLG.dSj(c, pad)
    
    for i in range(iters):
        for _ in range(additional_iters):
            Sji = heun.step(c.dt, Sji, dSj)
        Sjn[i+1, ...] = LLG.shave(pad, Sji)

    # normalize for easier curve-fit
    xl = Sjn[0, 0, 0, 0]
    x = Sjn[:, 0, 0, 0] / xl

    #plot.quiver(Sjn, c.dt)
    tau, omega = curvefit(x, c.dt) 
    t = c.dt*np.arange(Sjn.shape[0])
    print(f"{omega = }\n{tau = }\ntau_calc = {1/(c.alpha * omega)}")
    plt.figure()
    plt.plot(t, x*xl)
    #plt.plot(t, y)
    #plt.plot(t, z)
    #plt.plot(t, np.linalg.norm(Sjn[:, 0, 0, :], axis=-1))
    plt.plot(t, xl*np.cos(omega * t) * np.exp(-t/tau), "--")
    plt.xlabel("ps")
    plt.ylabel("$S_j^{x}$")
    plt.legend(["Data", "Curve fit"])
    plt.title(f"Single particle, $\\alpha = {c.alpha}$")
    plt.show()
