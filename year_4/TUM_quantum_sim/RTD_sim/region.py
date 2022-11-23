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
