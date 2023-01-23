import numpy as np
from matplotlib import pyplot as plt

from TUM_quantum_sim.RTD_sim import RTD_SIM_LOGGER as logging
from TUM_quantum_sim.RTD_sim.material import Material
from TUM_quantum_sim.RTD_sim.region import Region
from TUM_quantum_sim.RTD_sim.system import System
from TUM_quantum_sim.RTD_sim import plot
from TUM_quantum_sim.RTD_sim import solver
from TUM_quantum_sim import constants

def main():
    logging.info("Initialising sim")

    AlGaAs = Material(0.3)
    GaAs = Material(0)

    w   = 5e-9 # [m]
    pad = 1e-9 # [m]
    regions = [
        Region(GaAs,    0,          pad),
        Region(AlGaAs,  pad,        pad+w),
        Region(GaAs,    pad+w,      pad+2*w),
        Region(AlGaAs,  pad+2*w,    pad+3*w),
        Region(GaAs,    pad+3*w,    pad+3*w+pad)
    ]
    sys = System(regions)
    sys.set_voltage(-0.1)


    #logging.info("Plotting the potential")
    #plot.potential(sys)
    #plot.effective_mass(sys)

    eV = 1
    logging.info(f"Plotting the probability density for E={eV}eV")
    #plot.probability_density(eV, sys, 1000)

    logging.info("Calculating transmission probability")
    Es = np.linspace(0, 1, 100) 
    Ts = []
    for E in Es:
        Ts.append(solver.T(E * constants.e0, sys, 1000))
    plt.figure()
    plt.plot(Es, Ts)
    plt.xlabel("[eV]")
    plt.show()

if __name__ == "__main__":
    main()
