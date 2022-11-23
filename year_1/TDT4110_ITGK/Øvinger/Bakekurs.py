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
#     <li ><a href="Geometri.ipynb">Geometri</a></li>
#     <li ><a href="Vitenskapelig%20notasjon.ipynb">Vitenskapelig notasjon</a></li>
#     <li ><a href="Tetraeder.ipynb">Tetraeder</a></li>
#     <li class="active"><a href="Bakekurs.ipynb">Bakekurs</a></li>
#     <li ><a href="James%20Bond%20and%20Operation%20round().ipynb">James Bond and Operation Round</a></li>
#     </ul>
#   </div>
# </nav>
# 
# # Bakekurs
# 
# **Læringsmål:**
# 
# * Printe ut tekst til skjerm på en fin måte
# 
# * Kalkulasjoner i Python
# 
# **Starting Out with Python:**
# 
# * Kap. 2.3
# 
# * Kap. 2.8
# 
# * Kap. 8
# 
# I denne oppgaven skal du beregne mengden ingredienser som trengs for å lage cookies og printe resultatet på et fint format. 
# 
# Du skal lage cookies og har en oppskrift som gir 48 cookies. Den oppskriften krever følgende ingredienser:
# 
# * 400 g sukker 
# * 320 g smør
# * 500 g sjokolade
# * 2 egg 
# * 460 g hvetemel 

# ## a)

# Spør brukeren om hvor mange cookies han eller hun ønsker å bake og skriv ut hvor mange ingredienser som trengs for å lage så mange cookies.
# 
# Eksempel på kjøring:
# 
#   
# ```python
# Hvor mange cookies ønsker du å bake? 24
# Antall cookies: 24 
# sukker(g): 200.0
# smør(g): 160.0
# sjokolade(g): 250.0
# egg: 1.0
# hvetemel(g): 230.0
# ```
#     
# ***Skriv koden din i blokka under.***

# In[23]:


n = int(input("Hvor mange cookies vil du bake? "))

ingredienser = {}
ingredienser['sukker(g)'] = 200/48
ingredienser['smør(g)'] = 320/48
ingredienser['sjokolade(g)'] = 500/48
ingredienser['egg'] = 2/48
ingredienser['hvetemel(g)'] = 460/48

print("For", n, "cookies trenger du:")
for x in ingredienser:
    print(x, str(float(ingredienser[x])*n).rjust(18-len(x)))


# #### Tips til oppgave a: Escape Character

# `\n` er nyttig å bruke her for å få en ny linje! Eks. `print(“hei\npå\ndeg”)` gir
# 
# **Utskrift**
#   
# ```
# hei  
# på  
# deg
# ```

# ## b)

# Be brukeren om hvor mange cookies han eller hun ønsker å lage tre ganger og skriv ut ingrediensene på en fin og elegant måte. Du trenger kun å skrive ut antall cookies, og hvor mye sjokolade og sukker som trengs i gram.
# 
# Eksempel på kjøring:
# 
#   
# ```python
# Hvor mange cookies vil du lage? 24
# og hvor mange cookies vil du lage nå? 48
# og hvor mange cookies vil du lage til slutt? 72
# Antall cookies:        sukker(g)    sjokolade(g)
# 24                         200.0           250.0
# 48                         400.0           500.0
# 72                         600.0           750.0
# ```
# 
# `rjust()` og `ljust()` er nyttige funksjoner her, men for å bruke dem må man først konvertere antall cookies til en streng vha. `str()`. Andre ting som kan være nyttig er `\t` som lager et innrykk i teksten.
# 
# ***Skriv koden din i blokka under.***

# In[26]:


a = int(input("Hvor mange cookies vil du bake? "))
b = int(input("Hvor mange cookies vil du bake i morgen? "))
c = int(input("Hvor mange cookies vil du bake neste uke? "))

ingredienser = {}
ingredienser['sukker(g)'] = 200/48
ingredienser['smør(g)'] = 320/48
ingredienser['sjokolade(g)'] = 500/48
ingredienser['egg'] = 2/48
ingredienser['hvetemel(g)'] = 460/48

print("Da trenger du: ")
print("Antall cookies:  ", a, str(b).rjust(8), str(c).rjust(8))
for x in ingredienser:
    print(x, str(float(ingredienser[x])*a).rjust(20-len(x)), 
          str(float(ingredienser[x])*b).rjust(8), 
          str(float(ingredienser[x])*c).rjust(8))


# #### ljust() og rjust()

# `streng.ljust(width)` returnerer strengen "left justified" i en streng av lengde `width`. `streng.rjust(width)` gjør det sammen bare at strengen blir "right justified". For eksempel blir `print('hei'.rjust(15))` til:
# 
#   
# ```python
#            hei      #teksten printes altså ut etter 12 white spaces, ettersom strengen har lengde 3
# ```
#     
# Du kan lese mer om `rjust()` og `ljust()` [her](https://docs.python.org/2/library/stdtypes.html?highlight=rjust#str.rjust). 
