"""

Properties of different regions of the semiconductor

"""

from dataclasses import dataclass

from RTD_sim.material import Material

@dataclass
class Region:

    material: Material
    start: float
    end: float

    def __hash__(self):
        return hash(self.material.x) + hash(self.start) + hash(self.end - self.start)