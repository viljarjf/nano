"""General config for data saving ect"""

import os

FILENAME_FORMAT = "eigen{}_l{}_sub{}.npy"

def data_filepath(filename: str) -> str:
    data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data"))
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    return os.path.join(data_path, filename)

def figure_filepath(filename: str) -> str:
    data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "figures"))
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    return os.path.join(data_path, filename)
