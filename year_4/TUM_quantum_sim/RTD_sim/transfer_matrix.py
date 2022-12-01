"""
Generate a transfer matrix for a constant-potential system
"""

import numpy as np

class TransferMatrix(np.ndarray):
    pass


def _M_shift(k1: float | complex, dz: float) -> TransferMatrix:
    """Matrix for shifting a potential to z=dz instead of z=0

    Args:
        k1 (float | complex): initial k
        dz (float): width of region

    Returns:
        TransferMatrix: right matrix for shifting
    """
    return np.array(
        [
            [np.exp(1j*k1*dz), 0], 
            [0, np.exp(-1j*k1*dz)]
        ]
    )

def _M0(k1: float | complex, k2: float | complex) -> TransferMatrix:
    """Create a transfer matrix for a given k transition at z=0

    Args:
        k1 (float | complex): initial k
        k2 (float | complex): final k

    Returns:
        TransferMatrix: 2x2 transfer matrix
    """
    return (1 / (2*k2)) * np.array(
        [
            [ k2 + k1, k2 - k1],
            [ k2 - k1, k2 + k1]
        ]
    )


def M(k1: float | complex, beta1: float | complex, beta2: float | complex, dz: float) -> TransferMatrix:
    """Create a transfer matrix for a given k transition at z=d.
    Assuming constant potential between z=0 and z=d

    Args:
        k1 (float | complex): initial k
        beta1 (float | complex): initial beta (k / m)
        beta2 (float | complex): final beta
        dz (float): width of region

    Returns:
        TransferMatrix: 2x2 transfer matrix
    """
    Ms = _M_shift(k1, dz)
    M0 = _M0(beta1, beta2)

    return M0 @ Ms
