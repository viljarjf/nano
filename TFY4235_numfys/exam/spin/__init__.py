"""Numerical calculations with spin stuff"""
__all__ = [
    "LLG",
    "IO",
    "heun",
    "plot",
    "DEFAULT_C"
]
from spin import LLG
from spin import IO
from spin import heun
from spin import plot

import numpy as np

DEFAULT_C = LLG.Const(
        J                   = 1,            # meV
        dz                  = 0.0,          # meV
        mu                  = 0.05788,      # meV/T
        B0                  = 1.72,         # T
        ndims               = 1,            # ~
        dimdir              = "x",
        periodic_boundary   = False,        # ~
        alpha               = 0.01,         # ~
        kB                  = 0.0862,       # meV/K
        gamma               = 0.176,        # 1/Tps
        dt                  = 0.001,        # ps
        T                   = 0             # K
    )

def tmp():
    print(__file__)
    c = DEFAULT_C.copy()
    c.alpha = 0.05
    c.dz = 0.1
    c.B0 = 0.0 # boring, everything turns upright
    c.periodic_boundary = True
    c.ndims = 2
    c.J = 0.5
    c.T = 4

    Sjn = IO.load(c)
    iters = 10000
    additional_iters = 10

    if Sjn is None:
        n = 60
        dSj = LLG.dSj(c)
        Sj0 = np.array([[[0, 0, 1] for _ in range(n)] for _ in range(n)])
        Sj0 = 1 - 2*np.random.random(Sj0.shape)
        Sji = heun.normalize(Sj0)#np.roll(Sj0, 30, axis=1)
        Sjn = np.zeros((iters+1, *Sji.shape))
        Sjn[0, ...] = Sji
        
        plot.quiver2D_realtime(Sj0, dSj, c.dt)
        return
        for i in range(iters):
            for _ in range(additional_iters):
                Sji = heun.step(c.dt, Sji, dSj)
            Sjn[i+1, ...] = Sji
        IO.save(c, Sjn)

    plot.quiver(Sjn, c.dt)
    plot.quiver_realtime(Sj0, dSj, c.dt)
    #plot.coords_single(Sjn, c.dt, 0, 50, block=False)
    #plot.coords_single(Sjn, c.dt, 0, 0, block=False)
    #plot.coords_single(Sjn, c.dt, 0, -1)
