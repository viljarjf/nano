import numpy as np
import matplotlib.pyplot as plt
import time

from numba import jit


@jit(nopython=True)
def energy(system, i, j, L):
    """Energy function of spins connected to site (i, j)."""
    return -1. * system[i, j] * (system[np.mod(i - 1, L), j] + system[np.mod(i + 1, L), j] +
                                 system[i, np.mod(j - 1, L)] + system[i, np.mod(j + 1, L)])


@jit
def prepare_system(L):
    """Initialize the system."""
    system = 2 * (0.5 - np.random.randint(0, 2, size=(L, L)))
    return system


@jit(nopython=True)
def measure_energy(system):
    L = system.shape[0]
    E = 0
    for i in range(L):
        for j in range(L):
            E += energy(system, i, j, L) / 2.
    return E


@jit(nopython=True)
def metropolis_loop(system, T, N_sweeps, N_eq, N_flips):
    """ Main loop doing the Metropolis algorithm."""
    E = measure_energy(system)
    L = system.shape[0]
    E_list = []
    for step in range(N_sweeps + N_eq):
        i = np.random.randint(0, L)
        j = np.random.randint(0, L)

        dE = -2. * energy(system, i, j, L)
        if dE <= 0.:
            system[i, j] *= -1
            E += dE
        elif np.exp(-1. / T * dE) > np.random.rand():
            system[i, j] *= -1
            E += dE

        if step >= N_eq and np.mod(step, N_flips) == 0:
            # measurement
            E_list.append(E)
    return np.array(E_list)


if __name__ == "__main__":
    """ Scan through some temperatures """
    # Set parameters here
    L = 4  # Linear system size
    N_sweeps = 5000  # Number of steps for the measurements
    N_eq = 1000  # Number of equilibration steps before the measurements start
    N_flips = 10  # Number of steps between measurements
    N_bins = 100  # Number of bins use for the error analysis

    T_range = np.arange(1.5, 3.1, 0.1)

    C_list = []
    system = prepare_system(L)
    for T in T_range:
        C_list_bin = []
        for k in range(N_bins):
            Es = metropolis_loop(system, T, N_sweeps, N_eq, N_flips)

            mean_E = np.mean(Es)
            mean_E2 = np.mean(Es**2)

            C_list_bin.append(1. / T**2. / L**2. * (mean_E2 - mean_E**2))
        C_list.append([np.mean(C_list_bin), np.std(C_list_bin) / np.sqrt(N_bins)])
        print(T, mean_E, C_list[-1])

    # Plot the results
    C_list = np.array(C_list)
    plt.errorbar(T_range, C_list[:, 0], C_list[:, 1])
    Tc = 2. / np.log(1. + np.sqrt(2))
    print(Tc)
    plt.axvline(Tc, color='r', linestyle='--')
    plt.xlabel('$T$')
    plt.ylabel('$c$')
    plt.show()

# The above plot is the heat capacity as a function of temperature, 
# calculated as the variance of the energy, divided by temperature squared 
# and normalised to the system size.

# At low temperatures, the spins are aligned as in a ferromagnet
# At high temperatures, the spins are disordered in a random fashion
# At the critical temperature, disorder starts to appear

    T_range = np.arange(1.5, 3.5, 0.1)
    L_range = [5, 10, 15, 20, 30, 50]
    N_sweeps = 50000
    N_eq = 10000
    plt.figure()
    E_ax = plt.subplot(1,2,1)
    C_ax = plt.subplot(1,2,2)
    for L in L_range:
        E_bins = []
        C_bins = []
        system = prepare_system(L)
        for T in T_range:
            Es = metropolis_loop(system, T, N_sweeps, N_eq, N_flips)

            mean_E = np.mean(Es)
            mean_E2 = np.mean(Es**2)

            E_bins.append(mean_E)
            C_bins.append(1. / T**2. / L**2 * (mean_E2 - mean_E**2))
        E_ax.plot(T_range, E_bins, label=f"{L}x{L}")
        C_ax.plot(T_range, C_bins, label=f"{L}x{L}")
    E_ax.set_xlabel("T")
    E_ax.set_ylabel("E")
    C_ax.set_xlabel("T")
    C_ax.set_ylabel("Cv")
    plt.legend()
    plt.show()

# The above plot shows that increasing the system size strongly affects the total energy,
# but all systems follow the same rough shape in the temperature axis. 
# The same is true for the heat capacity for temperatures around and above the critical

# I did not have time to implement the final tasks.
# I have investigated magnetization of a 2D spin lattice previously,
# although the numerics were not Monte-Carlo based.
# Furthermore, the system was modeled with the Heisenberg model, instead of the Ising model.
# From that, I found that <M> was stable and at its highest for low temperatures,
# and 0 for high temperatures.
# The critical temperature significantly increases with an applied magnetic field.

# The report for the above mentioned simulation is attached, 
# but only figures 16 and 17 are relevant.
