"""
Equations describing the system.
Pragmatix approximations, not precise analytical solutions
"""

from RTD_sim import constants as c

def delta_V(x: float) -> float:
    """Calculate the potential difference between pure GaAs and Al_xGa_1-xAs

    Args:
        x (float): Al amount

    Returns:
        float: [J] Potential difference. 
    """
    return  0.62 * c.e0 * (1.594*x + x *(1 - x) * (0.127 - 1.310*x)) 


def m_star(x: float) -> float:
    """Calculate the effective mass of an electron in the conduction band of Al_xGa_1-xAs

    Args:
        x (float): Al amount

    Returns:
        float: [kg] Effective mass of electron
    """
    return c.me * (0.067 + 0.0174*x + 0.145*x**2)


def k(E: float, V: float, m: float) -> float | complex:
    """Calculate the wave "vector"(1D) of an electron. Can be complex, if the barrier is too tall

    Args:
        E (float): Energy of the electron
        V (float): Potential experienced at that position
        m (float): Effective mass of the electron

    Returns:
        float | complex: wave vector
    """
    return (2*m*(E - V))**0.5 / c.hbar

