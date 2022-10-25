"""

Numerically solve the differential equation y' = f(y)
using Euler's method

"""
from lab.state import State

_DELTA_T = 0.0001    # integrator timestep

def step(state: State, t: float) -> State:
    """Calculate the state at time `t` with initial state `state`

    Args:
        state (State): initial state
        t (float): final time

    Returns:
        State: new state
    """
    _t = 0
    _s = state
    while _t < t:
        # workaround for edge-case of solver:
        # one local timestep overshoots requested time
        if _t + _DELTA_T >= t:
            timestep = t - _t
        else:
            timestep = _DELTA_T
        
        d_s = state.derivative()

        _s = _s + d_s * timestep
        _t += timestep
    return _s
   