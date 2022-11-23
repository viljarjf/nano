from RTD_sim import RTD_SIM_LOGGER as logging

from RTD_sim.material import Material
from RTD_sim.region import Region
from RTD_sim.system import System
from RTD_sim import plot

def main():
    logging.info("Initialising sim")

    AlGaAs = Material(0.3)
    GaAs = Material(0)

    w   = 5 # [nm]
    pad = 1 # [nm]
    regions = [
        Region(GaAs,    0,          pad),
        Region(AlGaAs,  pad,        pad+w),
        Region(GaAs,    pad+w,      pad+2*w),
        Region(AlGaAs,  pad+2*w,    pad+3*w),
        Region(GaAs,    pad+3*w,    pad+3*w+pad)
    ]
    sys = System(regions)

    plot.potential(sys)

    sys.set_voltage(-0.1)
    plot.potential(sys)

if __name__ == "__main__":
    main()
