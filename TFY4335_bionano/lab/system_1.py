import os
from dataclasses import dataclass
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import random # for random color

METERS_PER_PIXEL = 0.25*10**-6
FPS = 7.5
D_TIMES_R = 2.08 * 10**-19 # product of diffusion coefficient and hydrodynamic radius


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
        dx = (p[0] - p0[0])*METERS_PER_PIXEL
        dy = (p[1] - p0[1])*METERS_PER_PIXEL
        D = (dx**2 + dy**2)/2*FPS
        Ds.append(D)
        p0 = p
    
    # Maximum likelihood estimators for a log-normal distribution
    log_D = np.log(Ds)
    mu = np.mean(log_D)
    sigma = np.std(log_D)
    return np.exp(mu + 0.5*sigma**2), (np.exp(sigma**2)-1)*np.exp(2*mu + sigma**2)**0.5


def get_r(file: str) -> list[float]:
    data = pd.read_csv(file)
    return data.iloc[:, 1].values


def main():

    # ylims for each subplot
    lims = {
        "A": [100, 80, 3300],
        "B": [359, 800, 13000]
        }
        
    curdir = os.path.dirname(__file__)
    for l in "AB":
        plt.figure()
        dlim, rlim, rrlim = lims[l]
        D_avg = []
        r_avg = []
        r_ravg = []
        for i in range(1,4):
            fileext = f"{i}{l}"
            data = readfile(os.path.join(curdir, f"Traj_DF_40x_7.5fps_{fileext}.txt"))
            Ds = []
            # filter a little
            for path, size in data:
                if size > 6:
                    m, s = get_D(path)
                    r = D_TIMES_R / m

                    # fairly arbitrary limits to make the plots nice
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
            plt.hist(D_TIMES_R / Ds[:,0]*10**6, bins = 50)
            if i == 2:
                plt.title("Hydrodynamic radii (µm)")
            plt.xlim([0,1])
            plt.ylim([0, rlim])
            plt.text(0.9, 0.8, fileext, transform=plt.gca().transAxes)

            csv = os.path.join(curdir, f"{fileext}.csv")
            r_real = get_r(csv)**0.5 * METERS_PER_PIXEL/ 3.14159 # transform pixel area to meter radius
            r_real = r_real[r_real < 10**-6]
            plt.subplot(3, 3, 6+i)
            plt.hist(r_real*10**6, bins = 50)
            if i == 2:
                plt.title("Optical radii (µm)")
            plt.xlim([0,1])
            plt.ylim([0, rrlim])
            plt.text(0.9, 0.8, fileext, transform=plt.gca().transAxes)
            
            D_avg += [i*10**12 for i in Ds[:, 0]]
            r_avg += [10**6 * D_TIMES_R / i for i in Ds[:, 0]]
            r_ravg += [i*10**6 for i in r_real]

            D = np.mean(Ds[:, 0])
            D_var = np.std(Ds[:, 0])
            r = D_TIMES_R / D
            r_var = D_TIMES_R / D_var
            r_r = np.mean(r_real)
            r_rvar = np.std(r_real)
            print(f"{fileext} & {len(Ds)} & {D*10**12 :.2g} $\pm$ {D_var*10**12 :.2g} & {r*10**6 :.2g} $\pm$ {r_var*10**6 :.2g} & {r_r*10**6 :.2g} $\pm$ {r_rvar*10**6 :.2g} \\\\")

        plt.show()

        # plot total as well
        n_bins = 50
        color = "#ffa500" #"#"+"".join(random.choices("1234567890abcdef", k = 6))
        plt.figure()
        plt.subplot(1, 3, 1)
        plt.hist(D_avg, bins = n_bins, facecolor=color)
        plt.title("Diffusion coefficient (µm² / s)")
        plt.ylim([0, dlim*3])
        
        plt.subplot(1, 3, 2)
        plt.hist(r_avg, bins = n_bins, facecolor=color)
        plt.title("Hydrodynamic radii (µm)")
        plt.xlim([0,1])
        plt.ylim([0, rlim*3])

        plt.subplot(1, 3, 3)
        plt.hist(r_ravg, bins = n_bins, facecolor=color)
        plt.title("Optical radii (µm)")
        plt.xlim([0,1])
        plt.ylim([0, rrlim*3])

        plt.show()

if __name__ == "__main__":
    main()