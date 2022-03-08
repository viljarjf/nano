import os
import numpy as np

def get_data(data_filename: str = None, time_filename: str = None, cutoff: float = None, n: int = 1) -> "tuple[np.ndarray, np.ndarray]":
    """get data from a file

    Args:
        data_filename (str, optional): name of file in data folder. Defaults to "particles.npy"
        time_filename (str, optional): name of file containing time corresponding to data. Defaults to "time.npy"
        cutoff (float, optional): if provided, remove all data greater than cuttoff
        n (int, optional): return every n datapoint. Defaults to 1 (return all data)

    Returns:
        np.ndarray: list of data points
        np.ndarray: list of time points
    """
    path = os.path.dirname(__file__)

    if data_filename is None:
        data_filename = "particles.npy"
    data_filename = os.path.join(path, "..", "data", data_filename)

    data = np.load(data_filename)
    data = data[:,::n]

    if time_filename is None:
        time_filename = "time.npy"
    time_filename = os.path.join(path, "..", "data", time_filename)

    time = np.load(time_filename)
    time = time[:,::n]

    if cutoff is not None:
        time = np.delete(time, data > cutoff)
        data = np.delete(data, data > cutoff)

    return data, time
