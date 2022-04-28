"""Save data"""

import numpy as np

from fractal_drum.utils import __config as cfg

def eigen(l: int, sub: int, eigenvectors: np.ndarray, eigenvalues: np.ndarray):
    filename = cfg.FILENAME_FORMAT.format("vec", l, sub)
    filepath = cfg.data_filepath(filename)
    np.save(filepath, eigenvectors)
    filename = cfg.FILENAME_FORMAT.format("val", l, sub)
    filepath = cfg.data_filepath(filename)
    np.save(filepath, eigenvalues)