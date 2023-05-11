"""
Verify both algorighms with a cool animation
"""
# hack to import with single file execution
from __init__ import IsingModel

from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider

J = 1.0
Lx = Ly = 20
T = 1.5

metropolis_system = IsingModel(J, Lx, Ly)
sw_system = IsingModel(J, Lx, Ly)

fig, axes = plt.subplots(2,2)
(slider_ax, _), (metro_ax, sw_ax) = axes
fig.delaxes(_)

metro_ax.set_title("Metropolis")
metro_ax.set_xticks([])
metro_ax.set_yticks([])

sw_ax.set_title("Swendsen-Wang")
sw_ax.set_xticks([])
sw_ax.set_yticks([])

metro_im = metro_ax.matshow(metropolis_system.spin_array)
sw_im = sw_ax.matshow(sw_system.spin_array)

T_slider = Slider(slider_ax, 'Temperature ', valmin=0, valmax=5, 
             valinit=1, valfmt='%.2f K/k_B', facecolor='#cc7000')

def animation(_):
    metropolis_system.iterate_metropolis(T, Lx * Ly)
    metro_im.set_data(metropolis_system.spin_array)

    sw_system.iterate_swendsen_wang(T)
    sw_im.set_data(sw_system.spin_array)

    return metro_im, sw_im

def change_T(_):
    global T
    T = T_slider.val
T_slider.on_changed(change_T)

ani = FuncAnimation(fig, animation, blit=False, interval=50)
plt.show()
