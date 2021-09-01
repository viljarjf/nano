#!/usr/bin/env python
# coding: utf-8

# <nav class="navbar navbar-default">
#   <div class="container-fluid">
#     <div class="navbar-header">
#       <a class="navbar-brand" href="_Oving1.ipynb">Øving 1</a>
#     </div>
#     <ul class="nav navbar-nav">
#         <li><a href="Intro%20til%20jupyter.ipynb">Intro til Jupyter</a></li>
#       <li ><a href="Jeg%20elsker%20ITGK!.ipynb">Jeg elsker ITGK!</a></li>
#     <li ><a href="Kalkulasjoner.ipynb">Kalkulasjoner</a></li>
#     <li><a href="Input%20og%20variable.ipynb">Input og variable</a></li>
#     <li><a href="Tallkonvertering.ipynb">Tallkonvertering</a></li>
#     <li ><a href="Peppes%20Pizza.ipynb">Peppes Pizza</a></li>
#     <li class="active"><a href="Geometri.ipynb">Geometri</a></li>
#     <li><a href="Vitenskapelig%20notasjon.ipynb">Vitenskapelig notasjon</a></li>
#     <li><a href="Tetraeder.ipynb">Tetraeder</a></li>
#     <li><a href="Bakekurs.ipynb">Bakekurs</a></li>
#     <li ><a href="James%20Bond%20and%20Operation%20round().ipynb">James Bond and Operation Round</a></li>
#     </ul>
#   </div>
# </nav>
# 
# # Geometri
# 
# **Læringsmål:**
# 
# * Forstå at kode må være feilfri for å kjøre, og rette enkle syntaksfeil
# 
# * Debugging
# 
# **Starting Out with Python:**
# 
# * Kap. 2
# 
# I denne oppgaven skal vi rette feil i koden og endre utskriftsformat.
# 
# Norsklæreren din kunne utmerket godt lest en stil og forstått den på tross av noen småfeil, og til og med gitt god karakter hvis innholdet forøvrig var bra. Datamaskinen er ikke like tilgivende: I et Python-program må alt være pinlig nøyaktig, en enkelt skrivefeil kan være nok til at programmet slett ikke kjører.

# ## a)

# Rett alle syntaksfeilene i koden under slik at koden kjører uten problemer. Hver av syntaksfeilene her kan rettes ved å fjerne, legge til eller endre ett enkelt tegn, dvs. det er ikke nødvendig å gjøre større endringer i koden. Ved å kjøre programmet (velg ”Run” i menyen) og se på feilmeldinger vil du få hint om hvor hver enkelt syntaksfeil befinner seg.

# In[9]:


r = 5
print("Vi har en sirkel med radius", r)
omkrets = 2 * 3.14 * r
print("Omkretsen er", format(omkrets, '.2f'))
areal = 3.14 * r ** 2
print("Arealet er", areal)
h = 8
volum = areal * h
print("Sylinder med høyde", h, ": Volumet er", volum)


# Når koden fungerer bør du få følgende output:
# 
#   
# ```python
# Vi har en sirkel med radius 5
# Omkretsen er 31.400000000000002
# Arealet er 78.5
# Sylinder med høyde 8 : Volumet er 628.0
#     ```

# #### Hint

# Tenk på parenteser, fnutter, variabelnavn og (+/,) i kombinasjon av tekst og variabelnavn.

# #### Formatering av antall desimaler

# At omkretsen får en liten hale med ...002 skyldes at flyttall ikke kan lagres helt nøyaktig i dataens minne. Derfor kan det være ønskelig med kun to desimaler. Det er en innebygd funksjon i Python som tar seg av formatering og den ser slik ut: `format(tall, formatering)`. `tall` er her tallet som skal konverteres, dvs. omkretsen i eksempelet over, mens formatering går ut på hvordan man ønsker å formere tallet. Et eksempel er format`(2/3, ‘.3f’)` som gir `0.667`. 3-tallet indikerer at det ønskes 3 desimaler.

# ## b

# Endre koden fra **a)** til å skrive ut omkretsen med kun 2 desimaler. Dvs. at linje to over skal bli endret til Omkretsen er 31.40.
# 
# Kjøring av oppdatert kode:
# 
#   
# ```python
# Vi har en sirkel med radius 5
# Omkretsen er 31.40
# Arealet er 78.5
# Sylinder med høyde 8 : Volumet er 628.0
#     ```

# ## c)

# (frivillig vanskelig oppgave) I oppgave a får omkretsen verdien 31.400...002, hvorfor blir ikke omkretsen sin verdi lik 31.400...000?

# Dobbelklikk på teksten under og skriv svaret ditt der:

# 31.4 i det binære tallsystemet kan ikke representeres med endelig antall desimaler. Det blir 11111.0110011001100...
# Når det lagres, har det et endelig antall desimaler. Derfor blir det en liten diskrepans mellom den reelle verdien og det som ble lagret som et binært tall.
