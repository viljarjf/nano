"""Simulate X-ray diffraction"""
from XRD.pylattice import lattice as pylattice
from XRD.convert import LAMBDA

import numpy as np

def get_lattice_data(substance: str) -> "tuple[np.ndarray, np.ndarray]":
    if substance == "KCl":
        # Set up the crystal structure
        a = 6.36
        lattice = pylattice.FCC(a)
        basis = pylattice.Basis(
            [
            (b'K',[0, 0, 0]),
            (b'Cl',[0.5, 0.5, 0.5])
            ],
            l_const = a
        )
    elif substance == "NaCl":
        a = 5.63
        lattice = pylattice.FCC(a)
        basis = pylattice.Basis(
            [
            (b'Na',[0, 0, 0]),
            (b'Cl',[0.5, 0.5, 0.5])
            ],
            l_const = a
        )
    else:
        raise NotImplementedError("Only NaCl and KCl are supported")
    
    crystal = lattice + basis

    # Plot a simulated XRD with copper radiation
    scattering_data = pylattice.powder_XRD(crystal, LAMBDA)
    angles, values = pylattice.spectrumify(scattering_data, instr_broadening=0.2)

    mask = angles < 40
    return angles[mask], values[mask]
