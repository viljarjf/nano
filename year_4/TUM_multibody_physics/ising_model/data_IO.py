from .square_lattice import IsingModel
from .triangular_lattice import TriangularIsingModel
import numpy as np

import os
from pathlib import Path

DATA_FOLDER = Path(__file__).parent.parent / "ising_data"


def _get_filename(L: int, J: float = 0, T0: float = 1, Tn: float = 3.5, 
             N: int = 100, model: type[IsingModel] = IsingModel) -> str:
    out = f"{L=}_{J=:.1f}_{T0=:.1f}_{Tn=:.1f}_{N=}_"
    out += ("square" if model == IsingModel else "triangular")
    out = out.replace(".", "_")
    return out + ".npz"
    

def get_data(L: int, J: float = 0, T0: float = 1, Tn: float = 3.5, 
             N: int = 100, model: type[IsingModel] = IsingModel) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Get energies, magnetization, and temperature data for a given system size

    :param L: Lx = Ly = L, system size
    :type L: int
    :param J: Energy scaling, defaults to 0
    :type J: float, optional
    :param T0: lower temperature, defaults to 1
    :type T0: float, optional
    :param Tn: upper temperature, defaults to 3.5
    :type Tn: float, optional
    :param N: temperature steps, defaults to 100
    :type N: int, optional
    :param model: Ising model type, defaults to IsingModel
    :type model: type[IsingModel], optional
    :return: Energies, Magnetizations, Temperatures
    :rtype: tuple[np.ndarray, np.ndarray, np.ndarray]
    """

    filename = Path(DATA_FOLDER, _get_filename(L, J, T0, Tn, N, model))
    try:
        file = np.load(filename)
        return file["Es"], file["Ms"], file["Ts"]
    
    except (OSError, FileNotFoundError):
        system = IsingModel(1.0, L, L)
        Ts = np.linspace(T0, Tn, N)

        # do some thermalization
        for _ in range(100):
            system.iterate_swendsen_wang(Ts[0])

        Es, Ms = system.sweep_swendsen_wang(Ts, 200)
        Es, Ms, Ts = file["Es"], file["Ms"], file["Ts"]

        np.savez(filename, Es=Es, Ms=Ms, Ts=Ts)

        return Es, Ms, Ts
