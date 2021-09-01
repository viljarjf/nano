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
#     <li><a href="Ideel%20gasslov.ipynb">Ideel Gasslov</a></li>
#     <li><a href="Sammenhengende%20tallrekke.ipynb">Sammenhengende Tallrekke</a></li>
#     <li ><a href="Sortering.ipynb">Sortering</a></li>
#     <li class="active"><a href="Strengmanipulasjon.ipynb">Strengmanipulasjon</a></li>
#     <li ><a href="Kryptering.ipynb">Kryptering</a></li>
#     <li ><a href="Litt%20sjakk.ipynb">Litt Sjakk</a></li>
#     </ul>
#   </div>
# </nav>
# 
# # Strengmanipulasjon
# 
# **Læringsmål:**
# 
# * Strenger
# * Funksjoner
# * Lister
# * Løkker
# 
# **Starting Out with Python:**
# 
# * Kap. 8.3

# ### a)

# Lag funksjonen `find_substring_indexes` som tar inn to strenger som argumenter (str1 og str2). Funksjonen skal finne plasseringen til alle substrengene av str1 i strengen str2. Den første indeksen til hver forekomst av str1 som substreng i str2 skal samles i en liste, og denne listen skal returneres.  
# Funksjonen tar ikke hensyn til store og små bokstaver, altså vil str2 = "Is this the real life? Is this just fantasy?" ha 4 substrenger av str1 = "iS"; "**Is** th**is** the real life? **Is** th**is** just fantasy?".
# 
# **Eksempel på kjøring:**
# ```python
# str1 = "iS", str2 = "Is this the real life? Is this just fantasy?"
# output -> [0, 5, 23, 28]
#   
# str1 = "oo", str2 = "Never let you go let me go. Never let me go ooo"      #Legg merke til at 'ooo' telles som to substrenger av 'oo'!
# output -> [44, 45]
# ```
# 
# ***Skriv funksjonen i kodeblokken under og test at den fungerer som den skal:***

# In[ ]:


def find_substring_indexes(str1, str2):
    str1=str1.lower()
    str2=str2.lower()
    l=[]
    x=0
    while str1 in str2:
        l.append(str2.index(str1)+x)
        x+=str2.index(str1)+1
        str2=str2[str2.index(str1)+1:]
    return l
print(find_substring_indexes("iS", "Is this the real life? Is this just fantasy?"))


# ### b)

# Nå skal du lage en funksjon som tar inn tre strenger som argumenter (str1, str2 og str3). Funksjonen skal finne alle substrenger av str1 i str2, og returnere en streng der disse substrengene i str2 er endret til str3. (Dette skal gjøres uten å bruke innebygde funksjoner.)
# 
# **Eksempel på kjøring:**
# ```python
# str1 = "iS", str2 = "Is this the real life? Is this just fantasy?", str3 = "cool"
# output -> cool thcool the real life? cool thcool just fantasy?
#   
# str1 = "oo", str2 = "Never let you goooo let me goo. Never let me goo oooo", str3 = "cool"
# output -> Never let you gcoolcoolcool let me gcool. Never let me gcool coolcoolcool
# ```
# 
# ***Skriv funksjonen i kodeblokken under og test at den fungerer som den skal:***

# In[3]:


def swap_substrings(str1, str2, str3):
    str1=str1.lower()
    str2=str2.lower()
    str3=str3.lower()
    l=''
    x=0
    while str1 in str2:
        try:
            if str2[str2.index(str1)+1:].index(str1)!=0:
                l+=str2[:str2.index(str1)]
                l+=str3
                x+=str2.index(str1)+1
                str2=str2[str2.index(str1)+len(str1):]
            else:
                l+=str2[:str2.index(str1)]
                l+=str3
                x+=str2.index(str1)+1
                str2=str2[str2.index(str1)+1:]
        except:
                l+=str2[:str2.index(str1)]
                l+=str3
                l+=str2[str2.index(str1)+len(str1):]
                break
                
    return l
print(swap_substrings(str1 = "oo", str2 = "Never let you goooo let me goo. Never let me goo oooo", str3 = "cool"))
print(swap_substrings(str1 = "iS", str2 = "Is this the real life? Is this just fantasy?", str3 = "cool"))


# #### Hint

# Bruk funksjonen fra a).
