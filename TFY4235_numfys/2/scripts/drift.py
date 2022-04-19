"""Calculate drift stuff"""
import numpy as np


def drift(particles: np.ndarray, dt: float) -> float:
    dx = particles[:,1:] - particles[:,:-1]
    res = np.mean(dx, axis = 1) / float(dt)
    return res[~np.isnan(res)]

def average(particles: np.ndarray, dt: float) -> float:
    res = (particles[:,-1] - particles[:,0]) / float(dt)
    return res[~np.isnan(res)]
