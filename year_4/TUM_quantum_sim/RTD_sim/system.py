"""
Equations describing the system.

Pragmatix approximations, not precise analytical solutions
"""

from RTD_sim import constants as c
from RTD_sim.region import Region

from RTD_sim import RTD_SIM_LOGGER as logging


def _k(E: float, V: float, m: float) -> float | complex:
    """Calculate the wave "vector"(1D) of an electron. Can be complex, if the barrier is too tall

    Args:
        E (float): Energy of the electron
        V (float): Potential experienced at that position
        m (float): Effective mass of the electron

    Returns:
        float | complex: wave vector
    """
    return (2*m*(E - V))**0.5 / c.hbar

class System:

    def __init__(self, regions: list[Region], voltage: float = None) -> None:
        """Set up a system. regions must be continuous and start at z=0

        Args:
            regions (list[Region]): continuous, non-overlapping, sorted list of regions
            voltage (float, optional): voltage between start and end. Defaults to None.

        Raises:
            ValueError: if regions are invalid
        """

        if voltage is None:
            self._U = 0
        else:
            self._U = voltage

        self._regions = regions
        if not self._validate_regions():
            raise ValueError("Invalid list of regions")
    
    def _validate_regions(self) -> bool:
        """Checks if the regions are continuous, non-overlapping and sorted

        Returns:
            bool
        """
        start = 0
        for r in self._regions:
            if r.start == start:
                start = r.end
            else:
                return False
        return True
            

    def _find_region(self, z: float) -> Region:
        """Returns the region at position z.
        
        If z is exactly at a boundary, use the lower-z region.

        Args:
            z (float): pos

        Returns:
            Region: region at z
        """
        if z > self.L or z < 0:
            raise ValueError("Not inside the system")
        
        for r in self._regions:
            if r.start <= z and r.end > z:
                return r
        return r # failsafe for z = L
        
    @property
    def E(self) -> float:
        """Electrical field"""
        return self._U / self.L
    
    @property
    def L(self) -> float:
        """Length of system"""
        return self._regions[-1].end

    
    def set_voltage(self, voltage: float) -> None:
        """Sets the potential difference of the system

        Args:
            voltage (float): [V] voltage between the ends
        """
        if float(voltage) == voltage:
            self._U = voltage
        else:
            raise ValueError("Not a valid potential")


    def add_region(self, region: Region) -> None:
        """Add a region to the system. 
        Assumes that the region has the same start as the previous end

        Args:
            region (Region): new region to add
        """
        if isinstance(region, Region):
            self._regions.append(region)
            if not self._validate_regions():
                self._regions.pop()
                raise ValueError("Invalid region for this system")
        else:
            raise ValueError("Not a region")

    def V(self, z: float) -> float:
        """Calculate the potential at position z

        Args:
            z (float): position

        Returns:
            float: potential 
        """
        r = self._find_region(z)
        return r.material.dV + z*self.E

    