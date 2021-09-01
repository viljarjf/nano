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
#     <li ><a href="Strengmanipulasjon.ipynb">Strengmanipulasjon</a></li>
#     <li class="active"><a href="Kryptering.ipynb">Kryptering</a></li>
#     <li ><a href="Litt%20sjakk.ipynb">Litt Sjakk</a></li>
#     </ul>
#   </div>
# </nav>
# 
# # Kryptering
# 
# **Læringsmål:**
# 
# * Lister
# * Tekstbehandling
# * Nettverkssikkerhet 
# 
# **Starting out with python:**
# 
# * Kap. 7: Lists and Tuples
# * Kap. 9.2: Sets
# 
# James Bond er på et topphemmelig oppdrag i Langtvekkistan for MI6. Han ønsker å kunne kommunisere med oppdragsgiveren sin via internett, men myndighetene i Langtvekkistan overvåker alt som sendes over nett i landet. Derfor må Bond og MI6 bruke noe som heter [kryptering](https://www.datatilsynet.no/regelverk-og-skjema/behandle-personopplysninger/kryptering/) (datatilsynet) når de kommuniserer, slik at de vet at ingen andre kan lese meldingene de sender seg i mellom. Oppdraget ditt er nå å lage denne krypteringen og for å gjøre det bruker vi en metode kalt "[One-time pad](https://en.wikipedia.org/wiki/One-time_pad)". Den fungerer slik: 
# 
# Krypteringen foregår ved at man har en melding M og en nøkkel K, og regner ut C definert under: 
# 
# * m = bokstav i ordet M
# * k = hemmelig bokstav fra ordet K
# * c = m [XOR](https://en.wikipedia.org/wiki/Exclusive_or) k (den krypterte bokstaven i C)
# (dvs. 1101 XOR 1011 = 0110)
# 
# For å dekryptere meldingen kan vi ved hjelp av passordet gjøre den motsatte operasjonen i og med at:
# 
# * m = c XOR k
# 
# Du kan fritt bruke disse hjelpefunksjoner i oppgaven:

# In[72]:


import binascii
 
def toHex(word):
    word=toBinary(word)
    return int(str(binascii.hexlify(word), 'ascii'), 16)
 
def toString(word):
    return str(binascii.unhexlify(hex(word)[2:]), 'ascii')

def toBinary(word):
    return bytes(word, encoding = 'ascii')
    


# `toHex` tar ikke inn en normal streng, men tar inn en binær streng. Koden nedenfor viser hvordan du konverterer en vanlig streng til binærstreng:
# 
# >```python
# string = bytes(string, encoding = 'ascii')
# ```

# ### a)

# Lag en funksjon `encrypt(message, key)` som tar inn en streng `message` og en nøkkel `key` (som er like lang som message, dvs. len(key)=len(message)) og returnerer det krypterte ordet ved å bruke XOR-operasjonen. 
# 
# Du må først gjøre om strengene `message` og `key` til heksadesimal v.h.a. funksjonen `toHex(word)` definert over. 
# 
# Funksjonen skal returnere heltallet `code` som er gitt ved M XOR K.
# 
# Hint: XOR i python implementeres med `^`-operatoren.
# 
# **Eksempel på kjøring:**
# >```python
# print(encrypt('hei','abc')) #msg='hei', key='abc'
# -> 591626
# ```
# 
# ***Skriv koden din i kodeblokken under og test at den fungerer:***

# In[90]:


def encrypt(message, key):
    return toHex(message)^toHex(key)


# ### b)

# Lag en funksjon `decrypt(code, key)` som tar inn en kode generert fra encrypt og nøkkelen **key**, og returnerer meldingen. 
# 
# Husk at M = C XOR K.
# 
# **Eksempel på kjøring:**
# >```python
# print(decrypt(591626,'abc')) #key = 'abc', code = 591626
# -> hei
# ```
# 
# ***Skriv koden din under og test at den fungerer:***

# In[94]:


def decrypt(code, key):
    return toString(code^toHex(key))
print(decrypt(591626,'abc'))


# #### Hint

# Her må du bruke både toHex og toString.

# ### c)

#  Lag en funksjon `main()` som tar inn en setning fra bruker, genererer en tilfeldig nøkkel, skriver ut den krypterte setningen og så den dekrypterte setningen.
#  
#  **Eksempel på kjøring.**
#  >```python
# Hva er meldingen? God dag, Bob Bernt
# Krypto: 8976018785527472660004435694777950941489408
# Melding: God dag, Bob Bernt
# ```
# 
# ***Skriv koden din under og test at den fungerer:***

# In[100]:


import random
def main():
    a=input('Hva er meldingen? ')
    key=''
    while len(key)<len(a):
        key+=random.choice('qwertyuiopasdfghjklzxcvbnm')
    print('Krypto:', encrypt(a, key))
    print('Melding:', a)
main()


# ### d) (frivillig)

# Dersom samme nøkkel blir brukt til å kryptere to forskjellige ord kan man bruke resultatet og en "ordbok" til å finne tilbake til de opprinnelige ordene, og derfor også nøkkelen. Forklar hvordan dette kan gjøres.

# 
