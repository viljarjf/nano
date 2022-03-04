import os

def get_data(filename: str = None) -> list:
    """get data from a file

    Args:
        filename (str, optional): name of file in data folder. Defaults to "particles.txt".

    Returns:
        list: list of data points
    """
    if filename is None:
        filename = "particles.txt"

    path = os.path.dirname(__file__)
    filename = os.path.join(path, "..", "data", filename)

    data = []
    with open(filename, "r") as f:
        for line in f:
            data.append(float(line))
    return data
