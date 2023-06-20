import numpy as np

from TUM_quantum_sim import constants as c


def static(z: float | np.ndarray, a: float, Vb: float) -> np.ndarray:
    """create a discretised array of the potential

    Args:
        z (float | np.ndarray): z coordinate in potential, [m]
        a (float): Potential function parameter, [m]
        Vb (float): Energy scaling, [J]

    Returns:
        float | np.ndarray: potential [J]
    """
    z0 = a / (4 * 2**0.5)
    return Vb * (-0.25 * (z / z0) ** 2 + 1 / 64 * (z / z0) ** 4)


def temporal(
    z: float | np.ndarray, t: float, E: float, omega: float
) -> float | np.ndarray:
    """Calculate the temporal evolution of the potential

    Args:
        z (float | np.ndarray): position [m]
        t (float): time [s]
        E (float): Electric field strength [V/m]
        omega (float): frequency, [rad/s]

    Returns:
        float | np.ndarray: potential [J]
    """
    return -c.e0 * E * z * np.sin(omega * t)


def total(
    z: float | np.ndarray, t: float, a: float, Vb: float, E: float, omega: float
) -> float | np.ndarray:
    """Calculate potential

    Args:
        z (float | np.ndarray): z coordinate in potential, [m]
        t (float): time [s]
        a (float): Potential function parameter, [m]
        Vb (float): Energy scaling, [J]
        E (float): Electric field strength [V/m]
        omega (float): frequency, [rad/s]

    Returns:
        float | np.ndarray: potential [J]
    """
    return static(z, a, Vb) + temporal(z, t, E, omega)
