"""Get data and stuff"""

import os
import shutil
import datetime
import glob
import numpy as np

def save() -> None:
    orig = os.path.join(os.path.dirname(__file__), "..", "data", "latest")

    file = glob.glob(os.path.join(orig, "*"))[0]
    time = os.path.getmtime(file)
    date = datetime.datetime.fromtimestamp(time)
    folder = date.strftime("%h%d_%H:%M")

    dest = os.path.join(orig, "..", folder)
    dest = os.path.abspath(dest)

    try:
        shutil.copytree(orig, dest, dirs_exist_ok=False)
    except FileExistsError:
        print(f"  Already saved in data/{folder}")


def get(filename: str, folder: str = None) -> "tuple[np.ndarray, np.ndarray]":
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
    if folder is None:
        folder = "latest"
    
    if "." not in filename:
        filename += ".npy"

    data_filepath = os.path.join(path, "..", "data", folder, filename)

    data = np.load(data_filepath)

    return data