"""Run the nuclear decay simulation and plot it"""
from nuclear import decay
from nuclear.decay.utils import steps, half_life

from matplotlib import pyplot as plt
import numpy as np


def plot_nuclear_decay(N0, lambdas, dt):
    Ns0 = [N0] + [0]*len(lambdas)
    Nsi = Ns0
    n = steps(lambdas[0], 0.001, dt)

    t = [0]
    Ns = [[Ns0i] for Ns0i in Ns0]
    for Nsi in decay.run(Nsi, lambdas, dt, n):
        t.append(t[-1] + dt)
        for i in range(len(Nsi)):
            Ns[i].append(Nsi[i])
    
    Nsa = [[] for _ in Ns0] + []
    for ti in t:
        Nsai = decay.run_analytical(N0, lambdas, ti)
        for i in range(len(Nsai)):
            Nsa[i].append(Nsai[i])

    
    plt.figure()
    for i, Nsi in enumerate(Ns):
        plt.plot(t, Nsi, label=f"{i}")
    for i, Nsi in enumerate(Nsa):
        plt.plot(t, Nsi, label=f"{i}", linestyle="--")
    plt.legend()
    plt.title(f"Nuclear decay over time\n$\\lambda_0 = {lambdas[0]}$, $\\lambda_1 = {lambdas[1]}$")
    plt.xlabel("Time")
    plt.ylabel("Amount")
    plt.show()

def main():
    N0 = 1000
    lambdas = [10, 2, 1]
    dt = 0.001
    for l in lambdas:
        print(f"lambda: {l}, Half-life: {half_life(l)}")
    plot_nuclear_decay(N0, lambdas, dt)
