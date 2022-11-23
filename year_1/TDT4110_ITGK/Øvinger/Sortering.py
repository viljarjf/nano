#!/usr/bin/env python
# coding: utf-8

# <nav class="navbar navbar-default">
#   <div class="container-fluid">
#     <div class="navbar-header">
#       <a class="navbar-brand" href="_Oving7.ipynb">Øving 7</a>
#     </div>
#     <ul class="nav navbar-nav">
#     <li ><a href="Aksessering.ipynb">Aksessering av karakter</a></li>
#     <li ><a href="Strenger%20og%20konkatinering.ipynb">Konkatinering</a></li>
#     <li ><a href="Slicing.ipynb">Slicing</a></li>
#     <li ><a href="Tekstbehandling.ipynb">Tekstbehandling</a></li>
#     <li ><a href="Strenghandtering.ipynb">Strenghåndtering</a></li>
#     <li ><a href="Innebygde%20funksjoner.ipynb">Innebygde funksjoner og lister</a></li>
#     <li ><a href="Fjesboka.ipynb">Fjesboka</a></li>
#     <li ><a href="Akkorder%20og%20toner.ipynb">Akkorder og toner</a></li>
#     <li ><a href="Ideel%20gasslov.ipynb">Ideel Gasslov</a></li>
#     <li><a href="Sammenhengende%20tallrekke.ipynb">Sammenhengende Tallrekke</a></li>
#     <li  class="active"><a href="Sortering.ipynb">Sortering</a></li>
#     <li ><a href="Strengmanipulasjon.ipynb">Strengmanipulasjon</a></li>
#     <li ><a href="Kryptering.ipynb">Kryptering</a></li>
#     <li ><a href="Litt%20sjakk.ipynb">Litt Sjakk</a></li>
#     </ul>
#   </div>
# </nav>
# 
# # Sortering
# 
# **Læringsmål:**
# 
# * Lister
# * Sortering
# 
# **Starting Out with Python:**
# 
# * Kap. 7: Lists and Tuples
# 
# Sortering av tall er en vanlig aktivitet i dataverden. Det er derfor utviklet mange mer eller mindre avanserte algoritmer for å gjøre dette effektivt (få antall beregninger). 
# 
# I denne oppgaven skal vi implementere to enkle sorteringsalgoritmer: [Bubble Sort](https://en.wikipedia.org/wiki/Bubble_sort) og [Selection Sort](https://en.wikipedia.org/wiki/Selection_sort). 

# ### a)

# Skriv funksjonen bubble_sort(list), forklart under.
# 
# * Så lenge listen er usortert:
#  * Gå gjennom hele listen
#    * Hvis elementet på plass i er større enn elementet på plass i+1
#      * Bytt plass på de to elementene
#      
# Funksjonen skal returnere den sorterte listen.
# 
# **Eksempel på kjøring:**
# ```python
# liste = [9,1,34,7,2,3,45,6,78,56,36,65,33,21,23,34,45,6]
# print(bubble_sort(liste))
# # Output blir:
# # [1, 2, 3, 6, 6, 7, 9, 21, 23, 33, 34, 34, 36, 45, 45, 56, 65, 78]
# ```
# 
# ***Skriv koden din i kodeblokken under:***

# In[15]:


def bubble_sort(liste):
    while not is_sorted(liste):
        for i in range(len(liste[:-1])):
            if liste[i]>liste[i+1]:
                liste[i],liste[i+1]=liste[i+1],liste[i]
    return liste


def is_sorted(liste):
    for i in range(len(liste[:-1])):
        if liste[i]>liste[i+1]:
            return False
    return True
    


# **Testkode**

# In[16]:


liste = [9,1,34,7,2,3,45,6,78,56,36,65,33,21,23,34,45,6]
print(bubble_sort(liste))


# ### b)

# Skriv funksjonen `selection_sort(list)`, forklart under.
# 
# * Lag en ny liste 
# * Gå gjennom hele den usorterte listen
#  * Finn det største tallet i den usorterte listen
#    * Legg dette inn fremst i den nye listen
#    * Fjern elementet fra den usorterte listen
#    
# Funksjonen skal returnere den sorterte listen.
# 
# **Eksempel på kjøring:**
# ```python
# liste = [9,1,34,7,2,3,45,6,78,56,36,65,33,21,23,34,45,6]
# print(selection_sort(liste))
# # Output blir:
# # [1, 2, 3, 6, 6, 7, 9, 21, 23, 33, 34, 34, 36, 45, 45, 56, 65, 78]
# ```
# 
# **Skriv koden din i kodeblokken under:**

# In[19]:


def selection_sort(liste):
    l=[]
    for i in range(len(liste)-1):
        l.append(min(liste))
        liste.remove(min(liste))
    return l


# **Testkode**

# In[20]:


liste = [9,1,34,7,2,3,45,6,78,56,36,65,33,21,23,34,45,6]
print(selection_sort(liste))


# ### c) (Frivillig)

# Hvilken av de to algoritmene er "best"/raskest til å sortere? Her kan det være lurt å lese seg opp på "store O".

# 
