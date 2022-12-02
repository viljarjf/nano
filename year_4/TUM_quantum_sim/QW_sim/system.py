from dataclasses import dataclass

@dataclass
class System:

    Lx: float
    Ly: float

    wire_x: float
    wire_y: float

    Nx: int
    Ny: int

    x: float
