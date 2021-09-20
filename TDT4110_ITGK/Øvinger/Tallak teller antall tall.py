#!/usr/bin/env python
# coding: utf-8

# <nav class="navbar navbar-default">
#   <div class="container-fluid">
#     <div class="navbar-header">
#       <a class="navbar-brand" href="_Oving9.ipynb">Øving 9</a>
#     </div>
#     <ul class="nav navbar-nav">
#     <li ><a href="Generelt%20om%20dictionary.ipynb">Generelt om dictionary</a></li>
#     <li ><a href="Innebygde%20funksjoner%20i%20dictionaries.ipynb">Innebygde funksjoner</a></li>
#     <li ><a href="Generelt%20om%20sets.ipynb">Generelt om sets</a></li>
#     <li ><a href="Generelt%20om%20filbehandling.ipynb">Generelt om filbehandling</a></li>
#     <li ><a href="Osteviruset.ipynb">Osteviruset</a></li>
#     <li ><a href="Bursdagsdatabasen.ipynb">Bursdagsdatabasen</a></li>
#     <li class="active"><a href="Tallak%20teller%20antall%20tall.ipynb">Tallak teller antall tall</a></li>
#     <li ><a href="Opptaksgrenser.ipynb">Opptaksgrenser</a></li>
#         <li ><a href="Soke%20i%20tekst.ipynb">Søke i tekst</a></li>
#     <li ><a href="Tre%20paa%20rad.ipynb">Tre på rad</a></li>
#     </ul>
#   </div>
# </nav>
# 
# # Tallak teller antall tall
# 
# **Læringsmål:**
# - Dictionary
# - Lese fra fil
# 
# **Starting Out with Python:**
# - Kap. 6: Files and Exceptions
# - Kap. 9: Dictionaries and Sets

# I denne oppgaven skal du hjelpe tallentusiasten Tallak med å lese inn data fra filen numbers.txt. Denne filen inneholder en liste med tall, noe som er Tallaks store lidenskap. Filen kan du se her: [numbers.txt](numbers.txt)

# ## a)
# Tallak ønsker først og fremst å få en oversikt over størrelsen på filen:
# 
# Lag funksjonen `number_of_lines(filename)` som returnerer totalt antall linjer i filen med navn `filename`. Test funksjonen med `numbers.txt`. Du bør få 36 som svar.
# 
# ***Skriv koden i kodeblokken under***

# In[3]:


def number_of_lines(filename):
    f=open(filename, 'r')
    res=f.read().count('\n')+1
    return res
print(number_of_lines('numbers.txt'))


# ## b)

# Tallak ønsker deretter en liste som inneholder antall forekomster av hvert enkelt tall i listen:
#     
# Lag funksjonen `number_frequency(filename)` som returnerer en dictionary der hver nøkkel er et tall, og verdien til en nøkkel er antall forekomster av det tallet i filen med navn `filename`. Test funksjonen med *numbers.txt*
# 
# ***Skriv koden i kodeblokken under***

# In[5]:


def number_frequency(filename):
    f=open(filename, 'r').read()
    res={}
    for x in range(1, 10):
        res[x]=f.count(str(x))
    return res
print(number_frequency('numbers.txt'))
    


# *Riktig utskrift:* `{7: 4, 4: 7, 9: 4, 1: 3, 3: 5, 5: 7, 2: 4, 6: 1, 8: 1}`

# ## c)

# Tallak er derimot ikke helt fornøyd med utskriften enda:
# 
# Kall funksjonen `number_frequency` på *numbers.txt*. For hvert tall i resultatet skal du skrive ut en linje med tallet sammen med antall forekomster, separart med et kolon.
# 
# **Eksempel på output fra kjøring:**
# ```
# 7: 4
# 4: 7
# 9: 4
# 1: 3
# 3: 5
# 5: 7
# 2: 4
# 6: 1
# 8: 1
# ```
# 
# PS: output trenger ikke å være sortert på noen måte.
# 
# ***Skriv koden din i kodeblokken under***

# In[7]:


a = number_frequency('numbers.txt')
for x in a:
    print(x,':', a[x])

