import numpy as np

from TUM_quantum_sim.QW_sim.system import System
from TUM_quantum_sim.utils import delta_V


def potential(sys: System) -> np.ndarray:
    """create a Nx x Ny array of potential

    Args:
        sys (System): the system parameters

    Returns:
        np.ndarray: 2D float array, [J]
    """

    # figure out where the wire is in the simulation area
    buffer_x = (sys.Lx - sys.wire_x) / 2
    buffer_y = (sys.Ly - sys.wire_y) / 2

    wire_Nx_min = int(sys.Nx * buffer_x // sys.Lx)
    wire_Ny_min = int(sys.Ny * buffer_y // sys.Ly)

    wire_Nx_width = int(sys.Nx * sys.wire_x // sys.Lx)
    wire_Ny_width = int(sys.Ny * sys.wire_y // sys.Ly)

    wire_Nx_max = wire_Nx_min + wire_Nx_width
    wire_Ny_max = wire_Ny_min + wire_Ny_width

    out = np.zeros((sys.Ny, sys.Nx))
    dV = delta_V(sys.x)

    out[wire_Ny_min:wire_Ny_max, wire_Nx_min:wire_Nx_max] = -dV

    return out
