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
#     <li class="active"><a href="Tetraeder.ipynb">Tetraeder</a></li>
#     <li><a href="Bakekurs.ipynb">Bakekurs</a></li>
#     <li ><a href="James%20Bond%20and%20Operation%20round().ipynb">James Bond and Operation Round</a></li>
#     </ul>
#   </div>
# </nav>
# 
# # Tetraeder 
# 
# **Læringsmål:**
# 
# * Input/output
# * Formatere utskreven tekst
# * Bruke innebygde funksjoner
# 
# **Starting Out with Python:**
# 
# * Kap. 2.8
# 
# ![img](./../../Resources/Images/Tetrahedron.jpg)
# 
# <br><br>I denne oppgaven skal du finne overflateareal og volum til regulære tetraedere (også kjent som trekantede pyramider). Et regulært tetraeder er et geometrisk objekt bestående av fire likesidede trekanter.
# 
# * **Overflatearealet til et tetraeder er A=$\sqrt{3}a^{2}$**  
# * **Volumet til et tetraeder er V=$\frac{\sqrt{2}a^{3}}{12}$  hvor a=$\frac{3}{\sqrt{6}}h$** 

# ## a)

# Lag et program som beregner og skriver ut på skjerm overflatearealet til et tetraeder. Test at programmet skriver ut 23.383 som resultat når høyden, h, er 3 (det gjør ikke noe om svaret får flere siffer).
# 
# Eksempel på kjøring:
#   
# ```python
# Et tetraeder med høyde 3 har areal 23.383
# ```
# 
# ***Skriv koden din i blokka under.***

# In[5]:


h = float(input("h= "))
h*=3/(6**0.5)
print("Et tetraeder med høyde", h/(3/(6**0.5)), "har areal", 3**0.5*h*h, "\nog volum lik", 2**0.5*h**3/12)


# #### Hint

# Kvadratrot kan regnes ut enten ved å opphøye et tall i 1/2, f.eks. `x ** 0.5`, eller ved `import math` og `math.sqrt` for å regne ut røttene. Det kan være lurt å lagre verdiene i variabler.

# ## b)

# Utvid programmet slik at det også skriver ut volumet til et tetraeder. Test at programmet skriver 5.846 når høyden (h) er 3 (det gjør ikke noe om svaret får flere siffer). Du kan skrive i samme kodeblokk som i oppgave a.
# 
# Eksempel på kjøring:
# 
#   
# ```python
# Et tetraeder med høyde 3 har volum 5.846
# ```

# ## c)

# Utvid programmet så brukeren blir bedt om å skrive inn verdien på høyden (h) fra tastaturet, og får ut volum og areal. Eksempel på kjøring vist i boksen under. Du kan skrive i samme kodeblokk som i oppgave a.
# 
# Eksempel på kjøring:
# 
#   
# ```python
# Skriv inn en høyde: 3
# Et tetraheder med høyde 3.0 har volum 5.85 og areal 23.38
# ```
