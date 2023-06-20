from dataclasses import dataclass

import matplotlib
import numpy as np
from qm_sim.hamiltonian import Hamiltonian

from TUM_quantum_sim.QW_sim import QW_SIM_LOGGER as logging
from TUM_quantum_sim.utils import delta_V, m_star


@dataclass
class System:
    Lx: float
    Ly: float
    wire_x: float
    wire_y: float
    Nx: int
    Ny: int
    x: float


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

    out = np.zeros((sys.Nx, sys.Ny))
    dV = delta_V(sys.x)

    out[wire_Nx_min:wire_Nx_max, wire_Ny_min:wire_Ny_max] = -dV

    return out


def main():
    matplotlib.use("QTagg")

    logging.info("Starting quantum wire simulation")

    s = System(Lx=40e-9, Ly=60e-9, wire_x=16e-9, wire_y=24e-9, Nx=60, Ny=90, x=0.1)

    H = Hamiltonian((s.Nx, s.Ny), (s.Lx, s.Ly), m_star(0))
    H.V = potential(s)

    H.plot_potential()
    H.plot_eigen(12)


if __name__ == "__main__":
    main()
