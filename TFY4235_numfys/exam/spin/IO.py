"""Save data"""

import numpy as np
from spin import __config as cfg
from spin.LLG import Const

from typing import Union

def save(c: Const, Sjn: np.ndarray, filename: str = None):
    if filename is None:
        filename = cfg.FILENAME_FORMAT.format(c.J, c.dz, c.B0, c.alpha, Sjn.shape)
    filepath = cfg.data_filepath(filename)
    np.save(filepath, Sjn)
    

def load(c: Const, filename: str = None) -> Union[np.ndarray, None]:
    if filename is None:
        filename = cfg.FILENAME_FORMAT.format(c.J, c.dz, c.B0, c.alpha)
    filepath = cfg.data_filepath(filename)
    try:
        return np.load(filepath)
    except IOError:
        return None
