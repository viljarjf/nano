from math import log
import matplotlib.pyplot as plt

def Stirling(n):
    return n*log(n) - n


N = 1.e10 #Lattice size 
lnN = Stirling(N)
Particles = range(int(1.e5), int(1.e10), int(1.e5)) #x-axis

W = [lnN - Stirling(n) - Stirling(N-n) for n in Particles] #Tip: Use list comprehension

plt.plot(Particles, W)
plt.title("$\\frac{S}{k_b}$ as a function of number of particles")
plt.ylabel("$\\frac{S}{k_b}$")
plt.xlabel("n")
plt.show()