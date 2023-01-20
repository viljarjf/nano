"""
Equations describing the system.

Pragmatix approximations, not precise analytical solutions
"""

from functools import lru_cache
import numpy as np

from TUM_quantum_sim import constants as c
from TUM_quantum_sim.RTD_sim.region import Region

from TUM_quantum_sim.RTD_sim import RTD_SIM_LOGGER as logging


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

    def __hash__(self):
        return sum(hash(r) for r in self._regions) + hash(self._U)
    
    def set_voltage(self, voltage: float) -> None:
        """Sets the potential difference of the system

        Args:
            voltage (float): [V] voltage between the ends
        """
        if float(voltage) == voltage:
            self._U = voltage
        else:
            raise ValueError("Not a valid potential")

    def set_electric_field(self, field: float) -> None:
        """Sets the electric field strength

        Args:
            field (float): Electric field, [V/m]
        """
        if float(field) == field:
            self._U = -field * self.L
        else:
            raise ValueError("Not a valid electric field")

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

    @lru_cache
    def _V(self, z: float) -> float:
        r = self._find_region(z)
        return r.material.dV + z*self.E*c.e0

    
    def V(self, z: float | np.ndarray) -> float | np.ndarray:
        """Calculate the potential at position z

        Args:
            z (float | np.ndarray): position

        Returns:
            float | np.ndarray: potential 
        """
        if isinstance(z, float) or isinstance(z, int):
            return self._V(z)
        elif isinstance(z, np.ndarray):
            return np.vectorize(self._V)(z)
        else:
            raise TypeError(f"Invalid type for argument 'z': {type(z)}")

    @lru_cache
    def m_star(self, z: float) -> float:
        """Get effective mass at position z

        Args:
            z (float): pos

        Returns:
            float: [kg] effective mass
        """
        return self._find_region(z).material.m


    @lru_cache
    def k(self, E: float, z: float) -> float | complex:
        """get wave number at position z

        Args:
            E (float): Inherent energy of wave
            z (float): pos

        Returns:
            float | complex: wave number. Complex if exponential decay instead of wave
        """
        m = self.m_star(z)
        return (2*m*(E - self.V(z)) + 0j)**0.5 / c.hbar


    def beta(self, E: float, z: float) -> float | complex:
        return self.k(E, z) / self.m_star(z)
