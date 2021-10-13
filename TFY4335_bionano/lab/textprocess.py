import os
from dataclasses import dataclass
import numpy as np
from matplotlib import pyplot as plt

@dataclass
class Point:
    """I did not want to convert everything to floats by rewriting stuff further down.
    This class is redundant now"""
    x: str
    y: str

    def __getitem__(self, i):
        if i == 0:
            return float(self.x)
        elif i == 1:
            return float(self.y)
        else:
            raise IndexError("Value out of range")


def readfile(filename: str) -> list[Point, float]:
    """read the file, and output the trajectory data. 
    Each element in the list is on the following format: 
    (list[Point], float)
    where the float is the amount of frames the trajectory took"""
    res = []
    cur_traj = []
    found_traj = False
    start_frame = 200
    end_frame = 0
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if "Trajectory" in line and "linking" not in line:
                res.append((cur_traj, end_frame - start_frame))
                found_traj = True
                cur_traj = []

            elif found_traj and line:
                sp = line.split(" ")
                end_frame = float(sp[0])
                start_frame = min(end_frame, start_frame)
                cur_traj.append(Point(
                    sp[1],
                    sp[2]
                ))
    return res[1:]


def get_ms(data: list[tuple]) -> float:
    """For a given list of points, find the mean of squared distances between concecutive points"""
    p0 = data.pop(0)
    res = 0
    for p in data:
        dx = (p[0] - p0[0])*0.25*10**-6
        dy = (p[1] - p0[1])*0.25*10**-6
        res += dx**2 + dy**2
        p0 = p
    return res / len(data)


def main():
    for fileext in ["1A", "2A", "3A", "1B", "2B", "3B"]:
        curdir = os.path.dirname(__file__)
        data = readfile(os.path.join(curdir, f"Traj_DF_40x_7.5fps_{fileext}.txt"))
        ms = []
        Ds = []
        for path, size in data:
            if size > 6:
                ms.append(get_ms(path))
                Ds.append(ms[-1] / 2 * 7.5/size)
        ms = np.array(ms)
        Ds = np.array(Ds)
        log_Ds = np.log(Ds)
        mu = np.mean(log_Ds)
        sigma = np.std(log_Ds)
        D = np.exp(mu + 0.5*sigma**2)
        D_var = (np.exp(sigma**2)-1)*np.exp(2*mu + sigma**2)**0.5
        r = 2.08 * 10**-19 / D
        r_var = 2.08 * 10**-19 / (np.exp(sigma**2)-1)*np.exp(-2*mu + sigma**2)**0.5
        print(f"{fileext} & {len(ms)} & {np.mean(ms)*10**12 :.2g} $\pm$ {np.std(ms)*10**12 :.2g} & {D :.2g} $\pm$ {D_var :.2g} & {r*10**6 :.2g} $\pm$ {r_var*10**6 :.2g} \\\\")

if __name__ == "__main__":
    main()