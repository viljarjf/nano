from RTD_sim import RTD_SIM_LOGGER as logging

from RTD_sim.material import Material
from RTD_sim.region import Region
from RTD_sim.system import System
from RTD_sim import plot
from RTD_sim import solver

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
    #sys.set_voltage(-0.1)


    logging.info("Plotting the potential")
    plot.potential(sys)


    eV = 0.2
    logging.info(f"Plotting the probability density for E={eV}eV")
    plot.probability_density(eV, sys, 1000)

    logging.info("Calculating transmission probability")
    T = solver.T(1, sys, 1000)
    logging.info(f"{T = }")

if __name__ == "__main__":
    main()
