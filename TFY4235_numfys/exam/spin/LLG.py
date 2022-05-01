"""Landau-Lifshitz-Gilbert equation"""
from __future__ import annotations
import numpy as np
import numba
from typing import Callable
from dataclasses import dataclass, replace

@dataclass
class Const:
        
    J: float
    dz: float 
    mu: float
    B0: float
    ndims: int
    dimdir: str
    periodic_boundary: bool
    alpha: float
    kB: float
    gamma: float
    dt: float
    T: float

    def copy(self) -> Const:
        return replace(self)
    

def pad(c: Const, Sj: np.ndarray) -> tuple[np.ndarray, tuple]:
    """Pad the input array according to the dimensions specified by c

    Args:
        c (Const): constants
        Sj (np.ndarray): data

    Returns:
        np.ndarray: Zero-padded data
        tuple: padding information
    """
    if c.periodic_boundary:
        if c.ndims == 1:
            if c.dimdir == "x":
                pad = ((0,0), (0,1), (0,0))
            elif c.dimdir == "y":
                pad = ((0,1), (0,0), (0,0))
        else:
            pad = ((0,0), (0,0), (0,0))
    else:
        pad = ((0,1), (0,1), (0,0))
    padded = np.pad(Sj, pad, mode='constant')
    return padded, pad

def shave(pad: tuple, Sj: np.ndarray) -> np.ndarray:
    """Shave off padding

    Args:
        pad (tuple): padding information
        Sj (np.ndarray): padded data

    Returns:
        np.ndarray: data
    """
    (_, xu), (_, yu), (_, _) = pad
    xm, ym, _ = Sj.shape
    return Sj[:xm - xu, :ym - yu, :]

@numba.jit(nopython=True, parallel=True)
def numba_wrap(Sj: np.ndarray, xmax: int, ymax: int) -> np.ndarray:
    """numba-accelerated neighbour-finder

    Args:
        Sj (np.ndarray): padded data
        xmax (int): x data size
        ymax (int): y data size

    Returns:
        np.ndarray: neighbour matrix
    """
    out = np.zeros(Sj.shape, dtype=Sj.dtype)
    for x in numba.prange(xmax):
        for y in numba.prange(ymax):
            out[x, y, :] = \
                Sj[x-1, y, :] + \
                Sj[x+1, y, :] + \
                Sj[x, y-1, :] + \
                Sj[x, y+1, :]
    
    xs, ys, _ = Sj.shape
    if xs == xmax:
        out[-1, :, :] = Sj[0, :, :]
    else:
        out[-1, :, :] = Sj[-1, :, :]
    if ys == ymax:
        out[:, -1, :] += Sj[:, 0, :]
    else:
        out[:, -1, :] += Sj[:, -1, :]
    
    return out

def F_eff(c: Const, pad: tuple) -> Callable[[np.ndarray], np.ndarray]:
    f0 = -c.J
    f1 = -2*c.dz
    f2 = -c.B0*c.mu*np.array([0, 0, 1])
    
    f = -1/c.mu

    (_, xu), (_, yu), (_, _) = pad
    
    def _F_eff(Sj: np.ndarray) -> np.ndarray:
        xmax, ymax, _ = Sj.shape
        term0 = f0 * numba_wrap(Sj, xmax - xu, ymax - yu)

        Sjz = Sj.copy()
        Sjz[..., :-1] = 0
        term1 = f1*Sjz + f2

        return f*(term0 + term1)

    return _F_eff


def F_th(c: Const) -> Callable[[np.ndarray], np.ndarray]:
    factor = ((2*c.alpha*c.kB*c.T)/(c.gamma*c.mu*c.dt))**0.5

    def _F_th(Sj: np.ndarray) -> np.ndarray:
        return factor * np.random.normal(size=Sj.shape).astype(Sj.dtype)

    return _F_th


def F(c: Const, pad: tuple) -> Callable[[np.ndarray], np.ndarray]:
    _F_eff = F_eff(c, pad)
    _F_th = F_th(c)

    return lambda Sj: _F_eff(Sj) + _F_th(Sj)

def dSj(c: Const, pad: tuple) -> Callable[[np.ndarray], np.ndarray]:
    _F = F(c, pad)
    a = c.alpha
    factor = -c.gamma / (1 + a**2)

    def _dSj(Sj: np.ndarray) -> np.ndarray:
        precession_term = np.cross(Sj, _F(Sj))
        damping_term = a*np.cross(Sj, precession_term)
        return factor * (precession_term + damping_term)
    
    return _dSj
