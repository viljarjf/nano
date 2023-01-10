"""

Describe potential and effective mass in a material

"""

from TUM_quantum_sim import utils


class Material:

    def __init__(self, x: float):
        self.x = x
        self.m = utils.m_star(x)
        self.dV = utils.delta_V(x)
