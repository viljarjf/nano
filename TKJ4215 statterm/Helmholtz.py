import numpy as np
from math import factorial, sqrt, exp, log
import matplotlib.pyplot as plt
import pickle

def Calculate_F(m_AB):
    States = list(set(m_AB)) #Creates a list of all macorstates
    States.sort() #Sorts the list according to increasing E
    Density_of_states = [m_AB.count(i) for i in States]#Should return a list of length = to len(States) with the density of each state. Use list comprehension
    Temp = np.linspace(0,10,5) #Sets the temperature range
    Legend = [] #Legend list for plotting purposes
    for T in Temp:
        F = [] #List of free energy valu for a given macrostate: to be appended 
        for U, W in zip(States, Density_of_states):
            F.append(U - T*log(W)) #Append the list

        plt.plot(States, F)
        Legend.append('Temp = %4.2f' % (T))
        
    plt.legend(Legend, loc='upper left')
    plt.savefig('Helmholtz_free_energy')
    plt.close()

with open('m_AB.pkl', 'rb') as f: #Opens up the list of all microstates.
    m_AB = pickle.load(f)[0] #m_AB is the list.

Calculate_F(m_AB)