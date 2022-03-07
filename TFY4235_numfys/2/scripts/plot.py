import os
import numpy as np

def get_data(filename: str = None, cutoff: float = None, n: int = 1) -> np.ndarray:
    """get data from a file

    Args:
        filename (str, optional): name of file in data folder. Defaults to "particles.txt".
        cutoff (float, optional): if provided, remove all data greater than cuttoff
        n (int, optional): return every n datapoint. Defaults to 1 (return all data)

    Returns:
        np.ndarray: list of data points
    """
    if filename is None:
        filename = "particles.npy"

    path = os.path.dirname(__file__)
    filename = os.path.join(path, "..", "data", filename)

    data = np.load(filename)
    data = data[:,::n]

    if cutoff is not None:
        data = np.delete(data, data > cutoff)

    return data
