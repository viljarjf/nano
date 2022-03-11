"""Functions to parse data from txt file"""
import os
import numpy as np

def get_data(filename: str = "data.txt") -> "list[np.ndarray]":
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

    return data
