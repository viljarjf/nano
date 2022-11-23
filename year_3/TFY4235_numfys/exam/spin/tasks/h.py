from spin import *

import numpy as np
from matplotlib import pyplot as plt

def M(Sj: np.ndarray) -> tuple[float, float]:
    """mean, std"""
    return np.mean(Sj[...,-1]), np.std(Sj[...,-1])

def run():
    print(__file__)
    c = DEFAULT_C.copy()
    c.alpha = 0.5
    c.periodic_boundary = True
    c.ndims = 2
    c.J = 1
    n = 10
    c.dt = 0.002

    iters = 1000
    additional_iters = 20

    Tmin = 0
    Tmax = 40
    dT = 4
    Trange = np.linspace(0, 50, 100) #np.arange(Tmin, Tmax+dT, dT)
    M_T_t = None#IO.load(None, f"M_T_t_alpha{0.5}_B0_{DEFAULT_C.B0}_Tmax_{25}.npy")
    if False:#M_T_t is None:
        M_T_t = []
        for T in Trange:
            print(f"{T = }")
            c.T = T
            M_t = []

            Sj0 = np.array([[[0, 0, 1] for _ in range(n)] for _ in range(n)])
            #Sj0 = np.random.uniform(size=Sj0.shape) + np.array([-0.5, -0.5, 0])
            #Sj0 = heun.normalize(Sj0)
            Sji, pad = LLG.pad(c, Sj0)

            dSj = LLG.dSj(c, pad)

            for _ in range(iters):
                for _ in range(additional_iters):
                    Sji = heun.step(c.dt, Sji, dSj)
                M_t.append(M(LLG.shave(pad, Sji)))
            M_T_t.append(M_t)
        
        M_T_t = np.array(M_T_t)
        IO.save(None, M_T_t, f"M_T_t_alpha{c.alpha}_J_{c.J}_Tmax_{Tmax}.npy")

    M_10 = IO.load(None, f"M_T_t_alpha{c.alpha}_J_{c.J}_Tmax_{Tmax}.npy")
    M_80 = IO.load(None, f"M_T_t_alpha{0.5}_B0_{DEFAULT_C.B0}_Tmax_{25}.npy")
    plt.figure()
    plt.subplot(211)
    plt.title("M(T,t), $n_x = n_y = 80$")
    trange = additional_iters*c.dt*np.arange(iters)
    plt.pcolormesh(trange, Trange, M_80[:, :, 0])
    plt.xlabel("Time (ps)")
    plt.ylabel("Temperature (K)")
    plt.colorbar()

    plt.subplot(212)
    plt.errorbar(Trange, np.mean(M_10[:, -100:, 0], axis=1), np.std(M_10[:, -100:, 0], axis=1))
    plt.errorbar(Trange, np.mean(M_80[:, -500:, 0], axis=1), np.std(M_80[:, -500:, 0], axis=1))
    plt.xlabel("Temperature (K)")
    plt.ylabel("M(T)")

    plt.title(f"M(T) at $\mathbf{{B}}$ =  ${c.B0}\mathbf{{e}}_z$ T")
    plt.legend([
        "$n_x = n_y = 10$",
        "$n_x = n_y = 80$"
    ])
    plt.tight_layout()
    plt.show()
    
    #plot.coords_single(Sjn, c.dt, 0, 50, block=False)
    #plot.coords_single(Sjn, c.dt, 0, 0, block=False)
    #plot.coords_single(Sjn, c.dt, 0, -1)
