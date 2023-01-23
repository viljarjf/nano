from TUM_quantum_sim.QW_sim import QW_SIM_LOGGER as logging

from TUM_quantum_sim.QW_sim import solver
from TUM_quantum_sim.QW_sim import physics
from TUM_quantum_sim.QW_sim.system import System
from TUM_quantum_sim import constants as c
from TUM_quantum_sim.utils import m_star

from qm_sim.hamiltonian import Hamiltonian

from matplotlib import pyplot as plt
import matplotlib
def main():

    matplotlib.use('QTagg')

    logging.info("Starting quantum wire simulation")

    s = System(
        Lx = 40e-9,
        Ly = 60e-9,
        wire_x = 16e-9,
        wire_y = 24e-9,
        Nx = 20,
        Ny = 30,
        x = 0.1
        )

    H = Hamiltonian((s.Nx, s.Ny), (s.Lx, s.Ly), m_star(0))
    V = physics.potential(s)
    
    H.set_static_potential(V)

    solutions = solver.eigen(s, H, n = 20)
    start_plot = 0

    plt.figure()
    for i in range(4*4):
        plt.subplot(4, 4, i+1)
        plt.imshow(solutions[start_plot + i].eigenvector)
        plt.title(f"{solutions[start_plot + i].eigenvalue / c.e0 :.3f} eV")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
