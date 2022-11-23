from spin import *

import numpy as np

def run():
    print(__file__)
    c = DEFAULT_C.copy()
    c.alpha = 0

    iters = 1000
    additional_iters = 100

    Sj0 = np.array([[[-0.2, 0, 0.8]]])
    Sj0 = heun.normalize(Sj0)

    Sji, pad = LLG.pad(c, Sj0)
    Sjn = np.zeros((iters+1, *Sj0.shape))
    Sjn[0, ...] = Sj0

    dSj = LLG.dSj(c, pad)
    
    for i in range(iters):
        for _ in range(additional_iters):
            Sji = heun.step(c.dt, Sji, dSj)
        Sjn[i+1, ...] = LLG.shave(pad, Sji)
        
    plot.coords_single(Sjn, c.dt*additional_iters, title=f"Single particle, $\\alpha = {c.alpha}$")
