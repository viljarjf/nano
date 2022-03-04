import os
import numpy as np

def get_data(filename: str = None, cutoff: float = None) -> np.ndarray:
    """get data from a file

    Args:
        filename (str, optional): name of file in data folder. Defaults to "particles.txt".
        cutoff (float, optional): if provided, remove all data greater than cuttoff

    Returns:
        np.ndarray: list of data points
    """
    if filename is None:
        filename = "particles.txt"

    path = os.path.dirname(__file__)
    filename = os.path.join(path, "..", "data", filename)

    data = []
    with open(filename, "r") as f:
        for line in f:
            data.append(float(line))
    data = np.array(data)

    if cutoff is not None:
        data = np.delete(data, data > cutoff)

    return data
