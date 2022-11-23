"""
Generate a transfer matrix for a constant-potential system
"""

import numpy as np

class TransferMatrix(np.ndarray):
    pass


def _T_shift(k2: float | complex, d: float) -> TransferMatrix:
    """Matrix for shifting a potential to z=d instead of z=0

    Args:
        k2 (float | complex): final k
        d (float): potential shift

    Returns:
        TransferMatrix: left matrix for shifting
    """
    return np.array(
        [
            [np.exp(1j*k2*d), 0], 
            [0, np.exp(-1j*k2*d)]
        ]
    )

def _T0(k1: float | complex, k2: float | complex) -> TransferMatrix:
    """Create a transfer matrix for a given k transition at z=0

    Args:
        k1 (float | complex): initial k
        k2 (float | complex): final k

    Returns:
        TransferMatrix: 2x2 transfer matrix
    """
    return (1 / (2*k2)) * np.array(
        [
            [ k2 + k2, k2 - k1],
            [ k2 - k1, k2 + k1]
        ]
    )


def Td(k1: float | complex, k2: float | complex, d: float) -> TransferMatrix:
    """Create a transfer matrix for a given k transition at z=d.
    Assuming constant potential between z=0 and z=d

    Args:
        k1 (float | complex): initial k
        k2 (float | complex): final k
        d (float): potential transition position

    Returns:
        TransferMatrix: 2x2 transfer matrix
    """
    Tl = _T_shift(k2, d)
    T0 = _T0(k1, k2)

    return Tl @ T0
