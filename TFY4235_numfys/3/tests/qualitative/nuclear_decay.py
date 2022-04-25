"""Run the nuclear decay simulation and plot it"""
from nuclear import decay
from nuclear.decay.utils import steps, half_life

from matplotlib import pyplot as plt


def plot_nuclear_decay(Ns0, lambdas, dt):
    Nsi = Ns0
    n = steps(lambdas[0], 0.001, dt)

    t = [0]
    Ns = [[Nsi[0]], [Nsi[1]], [Nsi[2]]]
    for _ in range(n):
        decay.run(Nsi, lambdas, dt)
        t.append(t[-1] + dt)
        Ns[0].append(Nsi[0])
        Ns[1].append(Nsi[1])
        Ns[2].append(Nsi[2])
    
    plt.figure()
    plt.plot(t, Ns[0])
    plt.plot(t, Ns[1])
    plt.plot(t, Ns[2])
    plt.legend(["0", "1", "2"])
    plt.title(f"Nuclear decay over time\n$\lambda_0 = {lambdas[0]}$, $\lambda_1 = {lambdas[1]}$")
    plt.xlabel("Time")
    plt.ylabel("Amount")
    plt.show()

def main():
    
    Ns0 = [1000, 0, 0]
    lambdas = [10, 2]
    dt = 0.001
    for l in lambdas:
        print(f"lambda: {l}, Half-life: {half_life(l)}")
    plot_nuclear_decay(Ns0, lambdas, dt)
