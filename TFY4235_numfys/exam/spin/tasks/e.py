from spin import *

import numpy as np


def run():
    print(__file__)
    c = DEFAULT_C.copy()
    c.alpha = 0.0
    c.ndims = 1
    c.dimdir = "y"
    c.periodic_boundary = True

    Sjn = None#IO.load(c)
    iters = 2000
    additional_iters = 10

    if Sjn is None:
        n = 30
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

    plot.imshow(Sjn.squeeze(), f"Simulation for $n_y = 10$ for {c.dt*iters*additional_iters}ps")
