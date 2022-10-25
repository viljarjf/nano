from lab.track import Track
from lab import plot
from lab.state import State
from lab.solver import step
from lab.dataclasses import Ball

def main():
    # Measured y-coordinates of each track point
    y_pos = [0.376, 0.352, 0.327, 0.251, 0.100, 0.244, 0.099, 0.251]

    # Create the track object
    track = Track(y_pos)

    # Plot the track and its derivative
    #plot.plot_track(track)

    # Set up state
    b = Ball(0.027, 0.4, 0.01)
    print(b)
    s = State(b, track)
    s.set_initial_condition(0.01, track(0) + b.r)

    print("Initial_state:", s.x, s.y)

    states = [s]
    stepsize = 0.01
    time = [0]
    while time[-1] < 1:
        s = step(s, stepsize)
        states.append(s)
        time.append(time[-1] + stepsize)

    plot.plot_pos_on_track(states, track)
    plot.plot_dist(states, time, track)
    plot.plot_energy(states, time, b)


if __name__ == "__main__":
    main()
