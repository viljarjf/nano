"""
Verify both algorighms with a cool animation
"""
# hack to import with single file execution
from __init__ import IsingModel

from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider

import numpy as np
import numba

J = 1.0
Lx = Ly = 40
T = 2 / np.log(1 + np.sqrt(2)) # Tc

@numba.njit
def running_mean(x: np.ndarray, N: int) -> np.ndarray:
    out = np.empty(x.shape)
    for i in range(N):
        out[i] = np.mean(x[i:i + N])
    for i in range(N, x.size):
        out[i] = np.mean(x[i - N:i + 1])
    return out


metro_system = IsingModel(J, Lx, Ly)
sw_system = IsingModel(J, Lx, Ly)

MAX_E_ELEMENTS = 1000
MAX_M_ELEMENTS = 1000

metro_E = np.zeros(MAX_E_ELEMENTS)
sw_E = np.zeros(MAX_E_ELEMENTS)
dummy_E_x = np.arange(MAX_E_ELEMENTS)

metro_M = np.zeros(MAX_M_ELEMENTS)
sw_M = np.zeros(MAX_M_ELEMENTS)
dummy_M_x = np.arange(MAX_M_ELEMENTS)

# Help the linter
axes: tuple[tuple[plt.Axes, plt.Axes], tuple[plt.Axes, plt.Axes], tuple[plt.Axes, plt.Axes]]

fig, axes = plt.subplots(3,2)
(slider_ax, _), (metro_ax, sw_ax), (M_ax, E_ax) = axes
fig.delaxes(_)

metro_ax.set_title("Metropolis")
metro_ax.set_axis_off()

sw_ax.set_title("Swendsen-Wang")
sw_ax.set_axis_off()

metro_im = metro_ax.matshow(metro_system.spin_array)
sw_im = sw_ax.matshow(sw_system.spin_array)

metro_E_plot, = E_ax.plot(dummy_E_x, metro_E, label="Metropolis")
sw_E_plot, = E_ax.plot(dummy_E_x, sw_E, label="Swendsen-Wang")

metro_M_plot, = M_ax.plot(dummy_M_x,  metro_M, label="Metropolis")
sw_M_plot, = M_ax.plot(dummy_M_x,  sw_M, label="Swendsen-Wang")

E_ax.set_title("E")
E_ax.legend()

M_ax.set_title("M")
M_ax.set_ylim(-1.1, 1.1)
M_ax.legend()

# fig.tight_layout()

T_slider = Slider(slider_ax, 'Temperature ', valmin=0, valmax=5, 
             valinit=T, valfmt='%.2f K/k_B', facecolor='#cc7000')

def animation(_):
    metro_system.iterate_metropolis(T, 3 * Lx * Ly)
    sw_system.iterate_swendsen_wang(T)

    metro_E[:] = np.roll(metro_E, -1, 0)
    metro_E[-1] = metro_system.E
    sw_E[:] = np.roll(sw_E, -1, 0)
    sw_E[-1] = sw_system.E

    metro_M[:] = np.roll(metro_M, -1, 0)
    metro_M[-1] = metro_system.M
    sw_M[:] = np.roll(sw_M, -1, 0)
    sw_M[-1] = sw_system.M

    metro_im.set_data(metro_system.spin_array)
    sw_im.set_data(sw_system.spin_array)

    # use running mean to lessen noise in plot
    metro_E_plot.set_data(dummy_E_x, running_mean(metro_E, 4))
    sw_E_plot.set_data(dummy_E_x, running_mean(sw_E, 4))
    # Use wider running mean for the noisier M
    metro_M_plot.set_data(dummy_M_x, running_mean(metro_M, 10))
    sw_M_plot.set_data(dummy_M_x, running_mean(sw_M, 10))

    E_ax.set_ylim(min(np.min(metro_E), np.min(sw_E)) * 1.1, max(np.max(metro_E), np.max(sw_E)) * 1.1)

    return metro_im, sw_im, metro_E_plot, sw_E_plot, metro_M_plot, sw_M_plot

def change_T(_):
    global T
    T = T_slider.val
T_slider.on_changed(change_T)

ani = FuncAnimation(fig, animation, blit=True, interval=50)
plt.show()
