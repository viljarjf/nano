"""

Calculate different forces 

"""
from math import sin, cos

from lab.dataclasses import Ball, Force, Point
from lab.track import Track

_G = 9.81

def gravity(ball: Ball) -> Force:
    return Force(0, -ball.m * _G)

def normal(pos: Point, vel: Point, ball: Ball, track: Track) -> Force:
    # m*(v^2 / r + g*cos(beta))

    # find contact point
    x = track.closest_point(pos)

    r = track.inverse_curvature(x)
    beta = track.angle(x)
    v2 = vel.len**2

    # magnitude
    f = ball.m * (v2 * r + _G*cos(beta))

    # direction
    direction = pos + Point(-x, -track(x))
    direction /= direction.len

    return direction * f


def air_resistance(v: Point, ball: Ball) -> Force:
    # -1/2 * rho * Cd * A * |v| * v
    # rho: air density = 1.2 kg/m^3
    # Cd: drag coefficient = 0.5 (for spheres)
    # A: frontal area = pi*r^2
    # v: speed
    
    # pre-calculate the constants
    return v * -0.942477 * ball.r**2 * v.len

def rolling_resistance(v: Point, k: float) -> Force:
    return v * -k

def zero_force() -> Force:
    return Force(0,0)