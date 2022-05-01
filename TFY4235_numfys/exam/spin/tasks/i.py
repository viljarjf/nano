from spin import *

import numpy as np
from matplotlib import pyplot as plt

def M(Sj: np.ndarray) -> tuple[float, float]:
    """mean, std"""
    return np.mean(Sj[...,-1]), np.std(Sj[...,-1])

def run():
    print(__file__)
    # fiddle with combining stored data with new generated data
    Bfs = [1/8, 1/2, 1, 2, 4]
    Tr1 = np.linspace(50, 100, 100) #([0] + [i/2+10 for i in range(0, 40)] + [40, 50])
    Tr2 = np.linspace(50, 100, 100) #([0, 10] + [i/2+20 for i in range(0, 40)] + [50])
    Tr3 = np.linspace(50, 100, 100) #([0, 10] + [i/2+20 for i in range(0, 40)] + [50])
    Tr4 = np.linspace(50, 100, 100) #([0, 15] + [i/2+30 for i in range(0, 40)])
    Tr5 = np.linspace(50, 100, 100) #([0, 15] + [i/2+30 for i in range(0, 40)])

    for Bf, Trange in zip(
        Bfs, 
        [Tr1, Tr2, Tr3, Tr4, Tr5]):
        
        c = DEFAULT_C.copy()
        c.alpha = 0.5
        c.periodic_boundary = True
        c.ndims = 2
        c.J = 1
        n = 80
        c.B0 *= Bf
        c.dt = 0.002

        iters = 1000
        additional_iters = 20

        Tmin = 0
        Tmax = 25
        dT = 10
        #Trange = np.arange(Tmin, Tmax+dT, dT)
        #Trange = np.array([0, 10, 20] + [i/2+25 for i in range(0, 32)])
        M_T_t = None#IO.load(None, f"M_T_t_alpha{c.alpha}_J_{c.J}_Tmax_{Tmax}.npy")
        if M_T_t is None:
            M_T_t = [i for i in IO.load(None, f"M_T_t_alpha{c.alpha}_B0_{c.B0}_Tmax_{Tmax}.npy")]
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
            IO.save(None, M_T_t, f"tmpM_T_t_alpha{c.alpha}_B0_{c.B0}_Tmax_{Tmax}.npy")

    M_1 = IO.load(None, f"tmpM_T_t_alpha{0.5}_B0_{DEFAULT_C.B0*Bfs[0]}_Tmax_{25}.npy")
    M_2 = IO.load(None, f"tmpM_T_t_alpha{0.5}_B0_{DEFAULT_C.B0*Bfs[1]}_Tmax_{25}.npy")
    M_3 = IO.load(None, f"tmpM_T_t_alpha{0.5}_B0_{DEFAULT_C.B0*Bfs[2]}_Tmax_{25}.npy")
    M_4 = IO.load(None, f"tmpM_T_t_alpha{0.5}_B0_{DEFAULT_C.B0*Bfs[3]}_Tmax_{25}.npy")
    M_5 = IO.load(None, f"tmpM_T_t_alpha{0.5}_B0_{DEFAULT_C.B0*Bfs[4]}_Tmax_{25}.npy")

    plt.figure()
    plt.title(f"$\\alpha = 0.5,\,n_x = n_y = 80$")

    plt.errorbar(Tr1, np.mean(M_1[:, -500:, 0], axis=1), np.std(M_1[:, -500:, 0], axis=1))
    plt.errorbar(Tr2, np.mean(M_2[:, -500:, 0], axis=1), np.std(M_2[:, -500:, 0], axis=1))
    plt.errorbar(Tr3, np.mean(M_3[:, -500:, 0], axis=1), np.std(M_3[:, -500:, 0], axis=1))
    plt.errorbar(Tr4, np.mean(M_4[:, -500:, 0], axis=1), np.std(M_4[:, -500:, 0], axis=1))
    plt.errorbar(Tr5, np.mean(M_5[:, -500:, 0], axis=1), np.std(M_5[:, -500:, 0], axis=1))
    
    plt.xlabel("Temperature (K)")
    plt.ylabel("M(T)")
    plt.legend([
        f"$\mathbf{{B}}$ =  ${Bfs[0]}B_0$", 
        f"$\mathbf{{B}}$ =  ${Bfs[1]}B_0$", 
        f"$\mathbf{{B}}$ =  ${Bfs[2]}B_0$", 
        f"$\mathbf{{B}}$ =  ${Bfs[3]}B_0$",
        f"$\mathbf{{B}}$ =  ${Bfs[4]}B_0$"])
    plt.tight_layout()
    plt.show()
        
        #plot.coords_single(Sjn, c.dt, 0, 50, block=False)
        #plot.coords_single(Sjn, c.dt, 0, 0, block=False)
        #plot.coords_single(Sjn, c.dt, 0, -1)
