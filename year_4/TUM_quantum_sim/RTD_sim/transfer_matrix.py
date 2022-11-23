"""
Generate a transfer matrix for a constant-potential system
"""

import numpy as np

class TransferMatrix(np.ndarray):
    pass


def _T_shift_LHS(k2: float | complex, d: float) -> TransferMatrix:
    """Left-hand matrix for shifting a potential to z=d instead of z=0

    Args:
        k2 (float | complex): final wave vector
        d (float): potential shift

    Returns:
        TransferMatrix: left matrix for shifting
    """
    return np.array(
        [
            [np.exp(complex(0, -k2*d)), 0], 
            [0, np.exp(complex(0, k2*d))]
        ]
    )


def _T_shift_RHS(k1: float | complex, d: float) -> TransferMatrix:
    """Right-hand matrix for shifting a potential to z=d instead of z=0

    Args:
        k2 (float | complex): final wave vector
        d (float): potential shift

    Returns:
        TransferMatrix: Right matrix for shifting
    """
    return np.array(
        [
            [np.exp(complex(0, k1*d)), 0], 
            [0, np.exp(complex(0, -k1*d))]
        ]
    )


def _T0(k1: float | complex, k2: float | complex) -> TransferMatrix:
    """Create a transfer matrix for a given wave vector transition at z=0

    Args:
        k1 (float | complex): initial wave vector
        k2 (float | complex): final wave vector

    Returns:
        TransferMatrix: 2x2 transfer matrix
    """
    return k2**-2 * np.array(
        [
            [ k2 + k2, k2 - k1],
            [ k2 - k1, k2 + k1]
        ]
    )


def T(k1: float | complex, k2: float | complex, d: float) -> TransferMatrix:
    """Create a transfer matrix for a given wave vector transition at z=d.
    Assuming constant potential between z=0 and z=d

    Args:
        k1 (float | complex): initial wave vector
        k2 (float | complex): final wave vector
        d (float): potential transition position

    Returns:
        TransferMatrix: 2x2 transfer matrix
    """
    Tl = _T_shift_LHS(k2, d)
    Tr = _T_shift_RHS(k2, d)
    T0 = _T0(k1, k2)

    return Tl @ T0 @ Tr
