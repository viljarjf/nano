from spin import *

import numpy as np


def run():
    print(__file__)
    c = DEFAULT_C.copy()
    c.alpha = 0.3
    c.ndims = 1
    c.dimdir = "y"

    Sjn = IO.load(c)
    iters = 1000
    additional_iters = 10

    if Sjn is None:
        n = 10
        Sj0 = np.array([[[-0.01, 0, 0.9], *[[0.0, 0, 0.9]]*(n-1)]])
        Sj0 = heun.normalize(Sj0)

        Sji, pad = LLG.pad(c, Sj0)
        Sjn = np.zeros((iters+1, *Sj0.shape))
        Sjn[0, ...] = Sj0

        dSj = LLG.dSj(c, pad)
        
        for i in range(iters):
            for _ in range(additional_iters):
                Sji = heun.step(c.dt, Sji, dSj)
            Sjn[i+1, ...] = LLG.shave(pad, Sji)
        #IO.save(c, Sjn)

    plot.quiver2D(Sjn, c.dt)
    plot.coords_multiple(Sjn, c.dt*additional_iters, f"1D particle line, $\\alpha={c.alpha}$, $dz={c.dz}$meV, $B_0={c.B0}$T", particles=range(10))
    t0 = c.dt*iters*additional_iters
    additional_iters = 100
    for i in range(iters):
            for _ in range(additional_iters):
                Sji = heun.step(c.dt, Sji, dSj)
            Sjn[i+1, ...] = LLG.shave(pad, Sji)
    plot.coords_multiple(Sjn, c.dt*additional_iters, f"1D particle line, $\\alpha={c.alpha}$, $dz={c.dz}$meV, $B_0={c.B0}$T", particles=range(10), t0=t0)

