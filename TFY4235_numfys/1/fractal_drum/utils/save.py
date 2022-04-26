"""Save data"""

import numpy as np

from fractal_drum.utils import __config as config

def eigen(l: int, sub: int, eigenvectors: np.ndarray, eigenvalues: np.ndarray):
    filename = config.FILENAME_FORMAT.format("vec", l, sub)
    filepath = config.data_filepath(filename)
    np.save(filepath, eigenvectors)
    filename = config.FILENAME_FORMAT.format("val", l, sub)
    filepath = config.data_filepath(filename)
    np.save(filepath, eigenvalues)