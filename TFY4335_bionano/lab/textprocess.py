import os
from dataclasses import dataclass
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

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
                f.readline()

            elif found_traj and line:
                sp = line.split(" ")
                end_frame = float(sp[0])
                start_frame = min(end_frame, start_frame)
                cur_traj.append(Point(
                    sp[1],
                    sp[2]
                ))
    return res[1:]


def get_D(data: list[Point]) -> tuple[float, float]:
    """For a given list of points, find the D. Return mu and sigma"""
    p0 = data.pop(0)
    Ds = []
    for p in data:
        dx = (p[0] - p0[0])*0.25*10**-6
        dy = (p[1] - p0[1])*0.25*10**-6
        D = (dx**2 + dy**2)/2*7.5
        if D < 10**-11:
            Ds.append(D)
        p0 = p
    log_D = np.log(Ds)
    mu = np.mean(log_D)
    sigma = np.std(log_D)

    return np.exp(mu + 0.5*sigma**2), (np.exp(sigma**2)-1)*np.exp(2*mu + sigma**2)**0.5

def get_r(file: str) -> list[float]:
    data = pd.read_csv(file)
    return data.iloc[:, 1].values

def main():
    lims = {
        "A": [100, 80, 3300],
        "B": [359, 800, 13000]
        }
    curdir = os.path.dirname(__file__)
    for l in "AB":
        plt.figure()
        dlim, rlim, rrlim = lims[l]
        for i in range(1,4):
            fileext = f"{i}{l}"
            data = readfile(os.path.join(curdir, f"Traj_DF_40x_7.5fps_{fileext}.txt"))
            Ds = []
            # filter a little
            for path, size in data:
                if size > 6:
                    m, s = get_D(path)
                    r = 2.08 * 10**-19 / m
                    if r < 10**-6 and m < 10**-11:
                        Ds.append((m, s))

            Ds = np.array(Ds)
        
            plt.subplot(3, 3, i)
            plt.hist(Ds[:,0]*10**12, bins = 50)
            if i == 2:
                plt.title("Diffusion coefficient (µm² / s)")
            plt.ylim([0, dlim])
            plt.text(0.9, 0.8, fileext, transform=plt.gca().transAxes)
            
            plt.subplot(3, 3, 3+i)
            plt.hist(2.08 * 10**-19 / Ds[:,0]*10**6, bins = 50)
            if i == 2:
                plt.title("Hydrodynamic radii (µm)")
            plt.xlim([0,1])
            plt.ylim([0, rlim])
            plt.text(0.9, 0.8, fileext, transform=plt.gca().transAxes)

            csv = os.path.join(curdir, f"{fileext}.csv")
            r_real = get_r(csv)**0.5 * 0.25*10**-6 / 3.14159
            r_real = r_real[r_real < 10**-6]*10**6
            plt.subplot(3, 3, 6+i)
            plt.hist(r_real, bins = 50)
            if i == 2:
                plt.title("Optical radii (µm)")
            plt.xlim([0,1])
            plt.ylim([0, rrlim])
            plt.text(0.9, 0.8, fileext, transform=plt.gca().transAxes)
            

            D = np.mean(Ds[:, 0])
            D_var = np.std(Ds[:, 0])
            r = 2.08 * 10**-19 / D
            r_var = 2.08 * 10**-19 / D_var
            r_r = np.mean(r_real)
            r_rv = np.std(r_real)
            print(f"{fileext} & {len(Ds)} & {D*10**12 :.2g} $\pm$ {D_var*10**12 :.2g} & {r*10**6 :.2g} $\pm$ {r_var*10**6 :.2g} & {r_r :.2g} $\pm$ {r_rv :.2g} \\\\")

        plt.show()

if __name__ == "__main__":
    main()