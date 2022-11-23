"""
Generate a transfer matrix for a constant-potential system
"""

import numpy as np

class TransferMatrix(np.ndarray):
    pass


def _T_shift_LHS(beta2: float | complex, d: float) -> TransferMatrix:
    """Left-hand matrix for shifting a potential to z=d instead of z=0

    Args:
        beta2 (float | complex): final beta (k / m*)
        d (float): potential shift

    Returns:
        TransferMatrix: left matrix for shifting
    """
    return np.array(
        [
            [np.exp(complex(0, -beta2*d)), 0], 
            [0, np.exp(complex(0, beta2*d))]
        ]
    )


def _T_shift_RHS(beta1: float | complex, d: float) -> TransferMatrix:
    """Right-hand matrix for shifting a potential to z=d instead of z=0

    Args:
        beta1 (float | complex): initial beta (k / m*)
        d (float): potential shift

    Returns:
        TransferMatrix: Right matrix for shifting
    """
    return np.array(
        [
            [np.exp(complex(0, beta1*d)), 0], 
            [0, np.exp(complex(0, -beta1*d))]
        ]
    )


def _T0(beta1: float | complex, beta2: float | complex) -> TransferMatrix:
    """Create a transfer matrix for a given beta (k / m*) transition at z=0

    Args:
        beta1 (float | complex): initial beta (k / m*)
        beta2 (float | complex): final beta (k / m*)

    Returns:
        TransferMatrix: 2x2 transfer matrix
    """
    return (1 / (2*beta2)) * np.array(
        [
            [ beta2 + beta2, beta2 - beta1],
            [ beta2 - beta1, beta2 + beta1]
        ]
    )


def T(beta1: float | complex, beta2: float | complex, d: float) -> TransferMatrix:
    """Create a transfer matrix for a given beta (k / m*) transition at z=d.
    Assuming constant potential between z=0 and z=d

    Args:
        beta1 (float | complex): initial beta (k / m*)
        beta2 (float | complex): final beta (k / m*)
        d (float): potential transition position

    Returns:
        TransferMatrix: 2x2 transfer matrix
    """
    Tl = _T_shift_LHS(beta2, d)
    Tr = _T_shift_RHS(beta2, d)
    T0 = _T0(beta1, beta2)

    return Tl @ T0 @ Tr
