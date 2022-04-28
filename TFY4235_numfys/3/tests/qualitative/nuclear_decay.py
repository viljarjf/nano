"""Run the nuclear decay simulation and plot it"""
from nuclear import decay
from nuclear.decay.utils import steps, half_life

from matplotlib import pyplot as plt


def plot_nuclear_decay(N0, lambdas, dt):
    Ns0 = [N0] + [0]*len(lambdas)
    Nsi = Ns0
    n = steps(lambdas[0], 0.001, dt)

    t = [0]
    Ns = [[Ns0[0]], [Ns0[1]], [Ns0[2]]]
    for Nsi in decay.run(Nsi, lambdas, dt, n):
        t.append(t[-1] + dt)
        Ns[0].append(Nsi[0])
        Ns[1].append(Nsi[1])
        Ns[2].append(Nsi[2])
    
    Nsa = [[], [],[]]
    for ti in t:
        Nsai = decay.run_analytical(N0, lambdas, ti)
        print(Nsai)
        Nsa[0].append(Nsai[0])
        Nsa[1].append(Nsai[1])
        Nsa[2].append(Nsai[2])

    plt.figure()
    plt.plot(t, Ns[0])
    plt.plot(t, Ns[1])
    plt.plot(t, Ns[2])
    plt.plot(t, Nsa[0])
    plt.plot(t, Nsa[1])
    plt.plot(t, Nsa[2])
    plt.legend(["0", "1", "2", "Analytical 0", "Analytical 1", "Analytical 2"])
    plt.title(f"Nuclear decay over time\n$\lambda_0 = {lambdas[0]}$, $\lambda_1 = {lambdas[1]}$")
    plt.xlabel("Time")
    plt.ylabel("Amount")
    plt.show()

def main():
    N0 = 1000
    lambdas = [10, 2]
    dt = 0.001
    for l in lambdas:
        print(f"lambda: {l}, Half-life: {half_life(l)}")
    plot_nuclear_decay(N0, lambdas, dt)
