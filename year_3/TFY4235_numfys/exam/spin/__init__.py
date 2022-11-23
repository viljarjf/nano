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
