"""

Describe the state of the ball

"""
from __future__ import annotations

from lab.track import Track
from lab.dataclasses import Ball, Point
from lab import force

import numpy as np


# State space indices
_X   = 0     # x-position
_Y   = 1     # y-position
_VX  = 2     # x-velocity
_VY  = 3     # y-velocity
_T   = 4     # angle (theta)
_O   = 5     # angular velocity (omega)
_STATE_SPACE_SIZE = 6


class State:

    def __init__(self, ball: Ball, track: Track):
        """Initialize a state object for a given ball on a given track

        Args:
            ball (Ball): initialized ball
            track (Track): track for the ball
        """

        self._ball = ball
        self._track = track
        self._state = np.zeros(_STATE_SPACE_SIZE)
    

    def set_initial_condition(self, x0: float, y0: float) -> None:
        self._state[_X] = x0
        self._state[_Y] = y0


    def derivative(self) -> State:
        """Return a new state object of the derivative of the current one

        Returns:
            State: derivative of current state
        """
        d_state = State(self._ball, self._track)

        pos = Point(self.x, self.y)
        vel = Point(self.vx, self.vy)
        dist = self._track.distance(pos)

        # gravity
        Fg = force.gravity(self._ball)

        # air resistance
        Fa = force.air_resistance(vel, self._ball)

        # If ball is touching track
        if dist <= self._ball.r:
            # normal force
            Fn = force.normal(pos, vel, self._ball, self._track)
            
            # rolling resistance
            Fr = force.rolling_resistance(vel, 0.1)
        else:
            Fn = force.zero_force()
            Fr = force.zero_force()
            

        # N2
        a = (Fg + Fa + Fn + Fr) / self._ball.m
        d_omega = Fr.len * self._ball.r / self._ball.I


        d_state._state[_X]  += self.vx
        d_state._state[_Y]  += self.vy
        d_state._state[_VX] += a.x
        d_state._state[_VY] += a.y
        d_state._state[_T]  += self.omega
        d_state._state[_O]  += d_omega

        return d_state

    def __add__(self, other):
        if isinstance(other, State):
            out = State(self._ball, self._track)
            out._state = self._state + other._state
            return out
        raise NotImplementedError
    
    def __mul__(self, other):
        if isinstance(other, float):
            out = State(self._ball, self._track)
            out._state = self._state * other
            return out
        raise NotImplementedError

    @property
    def x(self) -> float:
        return self._state[_X]

    @property
    def y(self) -> float:
        return self._state[_Y]

    @property
    def vx(self) -> float:
        return self._state[_VX]

    @property
    def vy(self) -> float:
        return self._state[_VY]

    @property
    def theta(self) -> float:
        return self._state[_T]

    @property
    def omega(self) -> float:
        return self._state[_O]
