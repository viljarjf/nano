from spin import *

import numpy as np


def run():
    print(__file__)
    c = DEFAULT_C.copy()
    c.alpha = 0.5
    c.periodic_boundary = True
    c.ndims = 1
    c.dimdir = "y"
    c.dz = 0.1
    c.B0 = 0
    c.J = -1
    c.T = 0
    n = 50

    Sjn = None#IO.load(c)
    iters = 2000
    additional_iters = 10

    if Sjn is None:
        Sj0 = 1 - 2*np.random.uniform(size=(1, n, 3))
        Sj0 = heun.normalize(Sj0)

        Sji, pad = LLG.pad(c, Sj0)
        Sjn = np.zeros((iters+1, *Sj0.shape))
        Sjn[0, ...] = Sj0

        dSj = LLG.dSj(c, pad)
        #plot.quiver2D_realtime(Sj0, dSj, c.dt, substeps=additional_iters)
        
        for i in range(iters):
            for _ in range(additional_iters):
                Sji = heun.step(c.dt, Sji, dSj)
            Sjn[i+1, ...] = LLG.shave(pad, Sji)
        IO.save(c, Sjn)

    plot.imshow(Sjn.squeeze(), f"Simulation for $n_y = {n}$ for {c.dt*iters*additional_iters}ps")
    