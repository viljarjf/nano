from ast import Num
import numpy as np
from math import factorial, sqrt, exp, log
import matplotlib.pyplot as plt
import pickle

def Calculate_Q_exact(E, T):
    Boltzmann_factors = [exp(-e/T) for e in E]#Should return a list of all Boltzmann factors (e^(-E/T))
    return sum(Boltzmann_factors)#The function return the exact partition function, as a sum of all Boltzmann factors.

def Calculate_Q_approx(Number_of_particles, T):
    W = factorial(Number_of_particles)/(factorial(Number_of_particles//2))**2 #Should return the multiplicity of a system with N particle and N_A = N_B = N/2
    return W*exp(-Number_of_particles / T)  #The function should return the Bragg-Williams approximated partition function

def Partition_function_plot(m_AB, Number_of_particles): #This is the plotting function. You do not need to do anything to this function.
    Temp = np.linspace(1,10,100)
    Q_exact_list = []
    Q_approx_list = []
    Q_ratio = []


    for T in Temp:
        Q_exact = Calculate_Q_exact(m_AB, T)
        Q_approx = Calculate_Q_approx(Number_of_particles, T)
        Q_exact_list.append(Q_exact)
        Q_approx_list.append(Q_approx)
        Q_ratio.append(Q_exact/Q_approx)

    plt.plot(Temp, Q_exact_list)
    plt.plot(Temp, Q_approx_list)
    plt.legend(['Q_exact', 'Q_approx'], loc='upper left')
    plt.savefig('Parition_function')
    plt.close()
    plt.plot(Temp, Q_ratio)
    plt.legend(['Q_ratio'], loc='upper left')
    plt.savefig('Parition_function_ratio')
    plt.close()

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
    m_AB, N = pickle.load(f) #m_AB is the list, N is the system size.

Calculate_F(m_AB)
Partition_function_plot(m_AB, N)#Calls the plotting function.