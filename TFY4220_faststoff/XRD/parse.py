"""Functions to parse data from txt file"""
import os
import numpy as np

def get_data(filename: str = "data.txt", lim: float = None) -> "list[np.ndarray]":

    filepath = os.path.join(os.path.dirname(__file__), filename)

    with open(filepath, "r") as f:
        start = False
        data = []
        run = []
        for line in f:
            if "# mv" in line:
                start = not start
                if run:
                    while [] in run:
                        run.pop(run.index([]))
                    data.append(np.array(run))
                run = []
            elif start:
                # parse line
                run.append([float(i) for i in line.strip().split()])

    if not lim is None:
        a, b = data
        a = np.delete(a, a[:, 0] > lim, axis = 0)
        b = np.delete(b, b[:, 0] > lim, axis = 0)
        data = [a, b]
    return data

def get_calculated_peaks() -> np.ndarray:
    """returns an array of calculated 2theta-values of peaks
    for Si

    Returns:
        np.ndarray
    """
    return np.array([
        13,
        21.2,
        25,
        30.3,
        33.1
    ])
