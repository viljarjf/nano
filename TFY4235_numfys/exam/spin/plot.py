"""pretty plots"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

from spin import heun

def coords_single(Sjn: np.ndarray, dt: float, title: str = None, nx: int = 0, ny: int = 0, block: bool = True) -> None:
    """plot coordinates from single particle

    Args:
        Sjn (np.ndarray): data
        dt (float): timestep
        title (str, optional): title of plot. Defaults to None.
        nx (int, optional): x pos of particle. Defaults to 0.
        ny (int, optional): y pos of particle. Defaults to 0.
        block (bool, optional): block execution when showing plots. Defaults to True.
    """
    x = Sjn[:, nx, ny, 0]
    y = Sjn[:, nx, ny, 1]
    z = Sjn[:, nx, ny, 2]
    t = dt*np.arange(Sjn.shape[0])
    if title is None:
        title = f"{nx = }; {ny = }"
    plt.figure()
    plt.plot(t, x)
    plt.plot(t, y)
    plt.plot(t, z)
    plt.xlabel("ps")
    plt.ylabel("$S_j^{xyz}$")
    plt.legend(["x", "y", "z"])
    plt.title(title)
    plt.show(block=block)

def coords_multiple(Sjn: np.ndarray, dt: float, title: str, particles: list = "all", block: bool = True, t0: float = 0) -> None:
    """plot coordinates from particles

    Args:
        Sjn (np.ndarray): data
        dt (float): timestep
        title (str, optional): title of plot
        particles (list, optional): list of particle indices to plot. Defaults to "all"
        block (bool, optional): block execution when showing plots. Defaults to True.
    """
    if particles == "all":
        particles = range(Sjn.shape[2])
    t = dt*np.arange(Sjn.shape[0]) + t0
    plt.figure()
    for i in particles:
        plt.plot(t, Sjn[:, 0, i, 0])
        
    plt.xlabel("ps")
    plt.ylabel("$S_j^{x}$")
    plt.legend([i+1 for i in particles])
    plt.title(title)
    plt.tight_layout()
    plt.show(block=block)

def quiver(Sjn: np.ndarray, dt: float) -> None:
    """Nice 3D plot

    Args:
        Sjn (np.ndarray): data
        dt (float): timestep
    """
    x = np.arange(Sjn.shape[1])
    y = np.arange(Sjn.shape[2])
    z = np.arange(1)
    xx, yy, zz = np.meshgrid(x, y, z)

    xd = Sjn[..., 0:1]
    yd = Sjn[..., 1:2]
    zd = Sjn[..., 2:3]

    def update(n, q):
        n *= 5
        segments = np.array((
            xx.squeeze(), 
            yy.squeeze(), 
            zz.squeeze(), 
            xx.squeeze() + xd[n,...].squeeze(), 
            yy.squeeze() + yd[n,...].squeeze(), 
            zz.squeeze() + zd[n,...].squeeze()
            ))
        segments = segments.reshape(6,-1)
        q.set_segments([[[x, y, z], [u, v, w]] for x, y, z, u, v, w in zip(*list(segments))])
        return q,

    f = plt.figure()
    ax = f.add_subplot(projection="3d")

    ax.grid(False)
    ax.axis("off")

    ax.set_xlim((-1,Sjn.shape[1]))
    ax.set_ylim((-1,Sjn.shape[2]))
    ax.set_zlim((-1,Sjn.shape[3]))
    
    q = ax.quiver(xx, yy, zz, xd[0,...], yd[0,...], zd[0,...])
    anim = animation.FuncAnimation(f, update, fargs=(q,), interval=50, blit=False)
    plt.tight_layout()
    plt.show()


def quiver2D(Sjn: np.ndarray, dt: float) -> None:
    x = np.arange(Sjn.shape[1])
    y = np.arange(Sjn.shape[2])
    xx, yy = np.meshgrid(x, y)

    def update(n, q):
        q.set_UVC(Sjn[n, ..., 0], Sjn[n, ..., 1], Sjn[n, ..., 2])
        return q,

    f = plt.figure(figsize=(4,4), dpi=250)
    
    q = plt.quiver(xx, yy, Sjn[0, ..., 0], Sjn[0, ..., 1], Sjn[0, ..., 2])
    anim = animation.FuncAnimation(
        f, 
        update, 
        fargs=(q,), 
        interval=50, 
        frames=Sjn.shape[0],
        blit=False)
    plt.xlim((-1,Sjn.shape[1]))
    plt.ylim((-1,Sjn.shape[2]))
    plt.grid(False)
    plt.axis("off")
    plt.tight_layout()
    anim.save("test.gif", animation.PillowWriter(fps = 60))
    plt.show()

def quiver_realtime(Sj0: np.ndarray, dSj: np.ndarray, dt: float, substeps: int = 50) -> None:
    x = np.arange(Sj0.shape[0])
    y = np.arange(Sj0.shape[1])
    z = np.arange(1)
    xx, yy, zz = np.meshgrid(x, y, z)

    Sji = Sj0

    def update(n, q):
        for _ in range(substeps):
            Sji[...] = heun.step(dt, Sji, dSj)
        segments = np.array((
            xx.squeeze(), 
            yy.squeeze(), 
            zz.squeeze(), 
            xx.squeeze() + Sji[..., 0].squeeze(), 
            yy.squeeze() + Sji[..., 1].squeeze(), 
            zz.squeeze() + Sji[..., 2].squeeze()
            ))
        segments = segments.reshape(6,-1)
        q.set_segments([[[x, y, z], [u, v, w]] for x, y, z, u, v, w in zip(*list(segments))])
        return q, Sji

    f = plt.figure()
    ax = f.add_subplot(projection="3d")

    ax.grid(False)
    ax.axis("off")

    ax.set_xlim((-1,Sji.shape[0]))
    ax.set_ylim((-1,Sji.shape[1]))
    ax.set_zlim((-5,5))
    
    q = ax.quiver(xx, yy, zz, Sji[..., 0], Sji[..., 1], Sji[..., 2])
    anim = animation.FuncAnimation(f, update, fargs=(q,), interval=50, blit=False)
    plt.tight_layout()
    plt.show()


def quiver2D_realtime(Sj0: np.ndarray, dSj: np.ndarray, dt: float, substeps: int = 10):
    x = np.arange(Sj0.shape[0])
    y = np.arange(Sj0.shape[1])
    xx, yy = np.meshgrid(x, y)

    Sji = Sj0

    def update(n, q):
        print(Sji[0, 0, -1])
        for _ in range(substeps):
            Sji[...] = heun.step(dt, Sji, dSj)
        q.set_UVC(Sji[..., 0], Sji[..., 1], Sji[..., 2])
        return q,

    f = plt.figure()
    
    q = plt.quiver(xx, yy, Sji[..., 0], Sji[..., 1], Sji[..., 2])
    anim = animation.FuncAnimation(f, update, fargs=(q,), interval=10, blit=False)
    plt.tight_layout()
    plt.show()


def imshow(Sjn: np.ndarray, title: str):
    f = plt.figure()
    f.suptitle(title)

    plt.subplot(131)
    plt.imshow(Sjn[..., 0], aspect="auto")
    plt.xticks([])
    plt.yticks([])
    plt.ylabel("Time")
    plt.title("$S_{j,\,x}$")

    plt.subplot(132)
    plt.imshow(Sjn[..., 1], aspect="auto")
    plt.xticks([])
    plt.yticks([])
    plt.title("$S_{j,\,y}$")
    plt.xlabel("Particles")

    plt.subplot(133)
    im = plt.imshow(Sjn[..., 2], aspect="auto")
    plt.xticks([])
    plt.yticks([])
    plt.title("$S_{j,\,z}$")

    plt.show()
    