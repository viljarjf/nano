"""

Create plots of the track, path, forces ect

"""
from matplotlib import pyplot as plt
import numpy as np
from lab.state import State
from lab.dataclasses import Point, Ball
from lab.track import Track

x_min, x_max = 0, 1.4

def plot_track(track: Track) -> None:

    plt.figure()
    x = np.linspace(x_min, x_max, 100)

    plt.subplot(2, 1, 1)
    plt.plot(x, track(x))
    plt.title("Track position")
    plt.xlabel("x [m]")
    plt.ylabel("y [m]")

    plt.subplot(2, 1, 2)
    plt.plot(x, track.derivative()(x))
    plt.title("Track derivative")
    plt.xlabel("x [m]")
    plt.ylabel(r"$\frac{dy}{dx}$ [-]")

    plt.tight_layout()
    plt.show()

def plot_inverse_curvature(track: Track):
    plt.figure()
    x = np.linspace(x_min + 0.01, x_max, 100, endpoint=False)
    plt.plot(x, track.inverse_curvature(x))
    plt.show()


def plot_pos(states: list[State]):

    plt.figure()
    plt.plot([s.x for s in states], [s.y for s in states])
    plt.show()

def plot_vel(states: list[State], time: list[float]):

    plt.figure()
    plt.subplot(2,1,1)
    plt.plot(time, [s.vx for s in states])
    plt.xlabel("time")
    plt.ylabel("vx")
    plt.subplot(2,1,2)
    plt.plot(time, [s.vy for s in states])
    plt.xlabel("time")
    plt.ylabel("vy")
    plt.show()

def plot_dist(states: list[State], time: list[float], track: Track):

    plt.figure()
    plt.plot(time, [track.distance(Point(s.x, s.y)) for s in states])
    plt.xlabel("time")
    plt.ylabel("dist")
    plt.title("Distance to track")
    plt.show()

def plot_pos_on_track(states: list[State], track: Track):
    plt.figure()
    x = np.linspace(x_min, x_max, 100)
    plt.plot(x, track(x))
    plt.plot([s.x for s in states], [s.y for s in states])
    plt.legend(["Track", "Path"])
    plt.title("Track position")
    plt.xlabel("x [m]")
    plt.ylabel("y [m]")
    plt.show()

def plot_energy(states: list[State], time: list[float], ball: Ball):
    plt.figure()
    plt.plot(time, [0.5*ball.m*(s.vx**2 + s.vy**2) + ball.m*9.81*s.y for s in states])
    plt.xlabel("time")
    plt.ylabel("dist")
    plt.title("Energy")
    plt.show()