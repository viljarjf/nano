"""Load previous calculations"""

import logging
import numpy as np

from fractal_drum.utils import __config as cfg

def eigen(l: int, sub: int) -> tuple[np.ndarray, np.ndarray]:
    """Get eigenvalues and eigenvectors if they exist

    Args:
        l (int): _description_
        sub (int): _description_

    Returns:
        tuple[np.ndarray, np.ndarray]: _description_
    """
    try:
        filename = cfg.FILENAME_FORMAT.format("vec", l, sub)
        filepath = cfg.data_filepath(filename)
        vec = np.load(filepath)
        filename = cfg.FILENAME_FORMAT.format("val", l, sub)
        filepath = cfg.data_filepath(filename)
        val = np.load(filepath)
        return vec, val
    except IOError:
        logging.info(f"No stored data found for {l = } and {sub = }")
        return None
