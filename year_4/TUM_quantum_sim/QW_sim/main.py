from TUM_quantum_sim.QW_sim import QW_SIM_LOGGER as logging

from TUM_quantum_sim.QW_sim import solver
from TUM_quantum_sim.QW_sim import physics
from TUM_quantum_sim.QW_sim import matrix
from TUM_quantum_sim.QW_sim.system import System
from TUM_quantum_sim import constants as c

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

    H = matrix.hamiltonian(s)
    # it seems there is no extra boundary condition??
    # H = matrix.apply_boundary(s, H)

    # plt.figure()
    # plt.imshow(H.toarray() / c.e0)
    # plt.show()

    # plt.figure()
    # plt.imshow(physics.potential(s))
    # plt.show()
    

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
