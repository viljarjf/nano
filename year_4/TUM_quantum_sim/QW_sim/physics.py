import numpy as np

from QW_sim.system import System

def _bandgap(x: float) -> float:
    """band gap between GaAs and Al_xGa_1-xAs

    Args:
        x (float): Al amount

    Returns:
        float: eV
    """
    return  0.62 * (1.594*x + x *(1 - x) * (0.127 - 1.310*x)) 


def _effective_mass(x: float) -> float:
    """estimate effective mass of electron in AlGaAs

    Args:
        x (float): Al amount

    Returns:
        float: electron masses
    """
    return 0.067 + 0.0174*x + 0.145*x**2


def potential(sys: System) -> np.ndarray:
    """create a Nx x Ny array of potential

    Args:
        sys (System): the system parameters

    Returns:
        np.ndarray: 2D float array, eV
    """
    out = np.zeros((sys.Ny, sys.Nx))

    dV = _bandgap(sys.x)
    out += dV

    # figure out where the wire is in the simulation area
    buffer_x = (sys.Lx - sys.wire_x) / 2
    buffer_y = (sys.Ly - sys.wire_y) / 2

    wire_Nx_min = int(sys.Nx * buffer_x // sys.Lx)
    wire_Ny_min = int(sys.Ny * buffer_y // sys.Ly)

    wire_Nx_width = int(sys.Nx * sys.wire_x // sys.Lx)
    wire_Ny_width = int(sys.Ny * sys.wire_y // sys.Ly)

    wire_Nx_max = wire_Nx_min + wire_Nx_width
    wire_Ny_max = wire_Ny_min + wire_Ny_width


    out[wire_Ny_min:wire_Ny_max, wire_Nx_min:wire_Nx_max] = 0

    return out