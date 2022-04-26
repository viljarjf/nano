"""Get a lattice from here"""

import numpy as np


def generate(l: int, dtype: np.dtype = np.int32) -> np.ndarray:
    """Generates a lattice 

    Args:
        l (int): level

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
        x0, y0 = lattice[:, 0]

        for i, [x, y] in enumerate(np.roll(lattice, -1, 1).T):
            xdir = x - x0
            ydir = y - y0
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
    
    return lattice
