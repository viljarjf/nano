import numpy as np
import matplotlib.pyplot as plt
import pickle, time
from numba import jit
from sympy.utilities.iterables import multiset_permutations

def Lattice_shape(N): #The function determines the lattice shapes that you will be using in this exercise, given N particles.
    if N == 4:
        return (2,2)
    elif N == 6:
        return (2,3)
    elif N == 8:
        return (2,4)
    elif N == 12:
        return (3,4)
    elif N == 16:
        return (4,4)
    elif N == 20:
        return (5,4)
    elif N == 24:
        return (6,4)
    elif N == 30:
        return (6,5)

# jit oversetter til maskinkode, som gjør ting superraskt
# kan brukes på det meste av numpy. Måtte lage en shift-funksjonalitet selv tho
# Selve funksjonen shifter hele arrayen ett hakk opp i y_shift og ett hakk til venstre i x_shift,
# og xor-er de med Lattice. Det gir samme effekt som å xor-e hvert element med naboene og summe 
@jit(nopython = True) 
def Count_AB(Lattice):
    y_shift = np.concatenate((Lattice[-1:, :], Lattice[:-1, :]), axis = 0) ^ Lattice
    x_shift = np.concatenate((Lattice[:, -1:], Lattice[:, :-1]), axis = 1) ^ Lattice
    return np.count_nonzero(y_shift) + np.count_nonzero(x_shift) 


# denne er så syk nå at jeg nesten ikke skjønner den selv lengre
def generate(N):
    # ints: en liste av 2^(N/2-1) heltall, tuklet med så hvert tall er delt opp i to bytes
    # vi halverer antallet her ved å legge til den ferdige tellingen to ganger, siden resultatet er likt for logcal not
    ints = np.flip(np.arange(0, 2**(N//2-1), dtype = np.uint16).reshape(2**(N//2-1), 1).view(np.uint8), axis = 1)
    # perms: liste med alle mulige permutasjoner av lengde N/2, der element i har i antall "False"
    perms = [list(multiset_permutations(l)) for l in [[0]*i + [1] * (N//2-i) for i in range(N//2)]]
    # ints, og tolk tallene som en liste av bools heller enn et binært tall
    for v in np.unpackbits(ints, axis = 1)[:, -N//2:]:
        # kombiner hver mulige første halvdel av den fullstendige listen med alle mulige andre halvdeler 
        # slik at total mengde "True" er N/2
        for v_ in perms[np.count_nonzero(v)]:
            yield np.concatenate((v, v_))

    

def Create_arrays_and_count(Number_of_particles):
    shape = Lattice_shape(Number_of_particles)
    m_AB = []
    for config in generate(Number_of_particles): 
            e = Count_AB(config.reshape(shape))
            m_AB.append(e)
            m_AB.append(e) # skip checking !config (the logical not of config)
    return m_AB

Count_AB(np.array([[1,1,],[0,0]])) # compile the function
s = time.time()
for i in [4, 6, 8, 12, 16, 20, 24]: #You will be calculating the density of states for the given system size
    m_AB = Create_arrays_and_count(i) #Call the correct function to create a list of all possible configuration AB-interactions
    Available_microstates = list(set(m_AB)) #Finds all uniqe macrostates
    Available_microstates.sort() #Sorts this list in ascending order, for plotting purposes.
    m_AB_degeneracy = [m_AB.count(i) for i in Available_microstates]
    #For each macrostate, this list should return the degeneracy. Use list_comprehension and list.count()
    
    #Creates a bar chart of density of states: x-axis = microstate, y-axis = degeneracy
    y_pos = np.arange(len(Available_microstates))
    plt.bar(y_pos, m_AB_degeneracy)
    plt.xticks(y_pos, Available_microstates, fontsize=7, rotation=30)
    plt.savefig('Density_of_states' + str(i))
    plt.clf()

    #To compare the variance of density of states as system size increases, you must normalize the interaction energies (number of AB-interactions)
    Normalization_factor = max(Available_microstates)#The normalization factor should be the highest possible number of AB-interactions for a given system size
    Normalized_mAB = [i/Normalization_factor for i in Available_microstates]#Create a normalized version of m_AB by deviding each instance by the Normalization_factor
    print(np.var(Normalized_mAB)) #Calculate and print the variance of Normalized_mAB. Use np.var().
print(time.time() - s)

#Saves m_AB and i for future use for system size = i_max (in this case 24)
with open('m_AB.pkl', 'wb') as f:
    pickle.dump([m_AB,i], f)