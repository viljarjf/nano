"""Get a lattice from here"""

import numba
import numpy as np


def fractal(l: int, sub: int, dtype: np.dtype = np.uint32) -> np.ndarray:
    """Generates a lattice 

    Args:
        l (int): level
        sub (int): subdivision

    Returns:
        np.ndarray: dtype np.int32 or np.int64, shape (2, 4*8^l)
    """
    # clockwise order
    start = np.array([
        [0, 0, 1, 1],
        [0, 1, 1, 0]
    ], dtype=dtype)
    
    lattice = start

    for i in range(l):
        # ensure only positive numbers 
        lattice *= 4
        lattice += 1

        new_lattice = np.zeros((2, lattice.shape[1]*8), dtype=dtype)
        x0, y0 = lattice[:, -1]

        for i, [x, y] in enumerate(lattice.T):
            xdir = int(x) - x0
            ydir = int(y) - y0
            if xdir:
                xdir //= abs(xdir)
                ydir = xdir
            
                new_lattice[:, 8*i + 0] = [x0 + 0 * xdir, y0 + 0 * ydir]
                new_lattice[:, 8*i + 1] = [x0 + 1 * xdir, y0 + 0 * ydir]
                new_lattice[:, 8*i + 2] = [x0 + 1 * xdir, y0 + 1 * ydir]
                new_lattice[:, 8*i + 3] = [x0 + 2 * xdir, y0 + 1 * ydir]
                new_lattice[:, 8*i + 4] = [x0 + 2 * xdir, y0 + 0 * ydir]
                new_lattice[:, 8*i + 5] = [x0 + 2 * xdir, y0 - 1 * ydir]
                new_lattice[:, 8*i + 6] = [x0 + 3 * xdir, y0 - 1 * ydir]
                new_lattice[:, 8*i + 7] = [x0 + 3 * xdir, y0 + 0 * ydir]

            else:
                ydir //= abs(ydir)
                xdir = -ydir

                new_lattice[:, 8*i + 0] = [x0 + 0 * xdir, y0 + 0 * ydir]
                new_lattice[:, 8*i + 1] = [x0 + 0 * xdir, y0 + 1 * ydir]
                new_lattice[:, 8*i + 2] = [x0 + 1 * xdir, y0 + 1 * ydir]
                new_lattice[:, 8*i + 3] = [x0 + 1 * xdir, y0 + 2 * ydir]
                new_lattice[:, 8*i + 4] = [x0 + 0 * xdir, y0 + 2 * ydir]
                new_lattice[:, 8*i + 5] = [x0 - 1 * xdir, y0 + 2 * ydir]
                new_lattice[:, 8*i + 6] = [x0 - 1 * xdir, y0 + 3 * ydir]
                new_lattice[:, 8*i + 7] = [x0 + 0 * xdir, y0 + 3 * ydir]
                
            x0, y0 = x, y
    
        lattice = new_lattice
    
    return lattice * dtype(sub)

@numba.njit
def lattice(fractal: np.ndarray, subdivision: int = 2) -> np.ndarray:
    n = np.max(fractal)+1
    out = np.zeros((n, n), dtype=np.int8)

    # we do some traversal to figure out if we are inside or outside
    OUT = -1
    EDGE = 0
    IN = 1

    out += OUT

    # create boundary
    x0, y0 = fractal[:, -1]
    for x, y in fractal.T:
        dx = np.int16(x) - x0
        dy = np.int16(y) - y0
        for i in range(subdivision):
            out[x0 + i*np.sign(dx), y0 + i*np.sign(dy)] = EDGE
        x0, y0 = x, y

    # start in the middle, which we know is on the inside
    check = [(n//2, n//2)]
    while check:
        x, y = check.pop()
        if out[x, y] != OUT:
            continue
        out[x, y] = IN
        check.append((x + 1, y + 0))
        check.append((x - 1, y + 0))
        check.append((x + 0, y + 1))
        check.append((x + 0, y - 1))

    return out


def calc_n(l: int, sub: int) -> int:
    """Calculate n from the level and subdivision

    Args:
        l (int): fractal level
        sub (int): subdivision level

    Returns:
        int: size of grid
    """
    n0 = 1
    ni = lambda i: 4*ni(i-1) + 2 if i else n0
    nl = ni(l)
    n = nl * sub + 1
    return n
