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
#     <li class="active"><a href="Vitenskapelig%20notasjon.ipynb">Vitenskapelig notasjon</a></li>
#     <li><a href="Tetraeder.ipynb">Tetraeder</a></li>
#     <li><a href="Bakekurs.ipynb">Bakekurs</a></li>
#     <li ><a href="James%20Bond%20and%20Operation%20round().ipynb">James Bond and Operation Round</a></li>
#     </ul>
#   </div>
# </nav>
# 
# # Vitenskapelig notasjon
# 
# **Læringsmål:**
# 
# * Vitenskapelig notasjon for spesielt små og spesielt store flyttall
# 
# **Starting Out with Python:**
# 
# * Kap. 2.8

# ### Nyttig info om formatering av store tall

# Når vi skriver flyttall i Python, er det enkleste ofte å skrive tallet rett frem, for eksempel 9.80665 eller 0.0002. Hvis tallet blir veldig stort (~$10^{6}$) eller lite (~$10^{-6}$), er det derimot tidkrevende å skrive tallet fullt ut, samtidig som at det lett dukker opp slurvefeil. Da vil resultatet av en beregning bli helt feil. Derfor er det vanlig å bruke vitenskapelig notasjon for store og små tall.
# 
# I Python kan vi skrive tallene 3.0 × 10 $^{9}$ og 3.19 × 10$^{-10}$ ved bruk av multiplikasjon(`*`) og potensregning(`**`) slik: `3.0*10**9` og `3.19*10 **(-10)`. Det vil gi riktig resultat, men kaster bort tid og strøm på å gjøre helt unyttige beregninger, først en potensering, så en multiplikasjon, for å finne fram til et tall vi egentlig allerede vet hva er. Det er derfor bedre å bruke notasjonen `3.0e9` og `3.19e-10`, hvor tallet bak `e` viser tierpotensen for å uttrykke store og små tall. 
# 
# Notasjonen med `e` (som her ikke har noe med konstanten e å gjøre) lar oss legge tallet rett inn i variabelen uten noe regning. Eksemplet under viser bruk av denne notasjonen i linje 3.
# 
# Eksempel på kode (**Prøv å kjør koden!**)

# In[2]:


tid = float(input("Hva er din pers på 60m? "))
m_sek = 60/tid
lysfart = 3.0e8
x = lysfart / m_sek
print("Bra! Men for å nå igjen lyset...")
print("...må du løpe", x, "ganger fortere")
print("som også kan skrives", format(x, '.6e'), "ganger fortere.")


# `.1e` i format viser at det er ønskelig med én desimal i den vitenskapelige notasjonen. `.2e` ville gitt `4.25e+07`.

# ## a) Fysikk / kjemi

# Avogadros konstant 6.022 × 10<sup>23</sup> sier hvor mange molekyler av et stoff som fins i ett mol av stoffet. Lag et program som ber brukeren navngi et stoff hun er i besittelse av, oppgi hvilken molvekt dette stoffet har, og hvor mye av stoffet hun har, og så skriver ut på skjermen hvor mange molekyler brukeren har av stoffet. Bruk gjerne `format()`-funksjonen for å unngå for mange desimaler i svaret. 
# 
# Eksempel på kjøring:
# 
#   
# ```python
# Si et stoff du er i besittelse av: vann
# Hva er molvekt i gram for vann? 18
# Hvor mange gram vann har du? 500
# Du har 1.7e+25 molekyler vann
# ```
# 
# ***Skriv koden din i blokka under.***

# In[12]:


stoff = input("Si et stoff du er i besittelse av: ")
molar_masse = float(input("Hva er molvekt i gram for "+stoff+ "?" ))
masse = float(input("Hvor mange gram "+stoff+" har du? "))
avogadros_konstant = 6.022e23
antall_molekyler = format(avogadros_konstant*masse/molar_masse, '.1e')
print("Du har",antall_molekyler,"molekyler", stoff)


# #### Hint

# Hint 1: `print("...må du løpe", x, "ganger fortere")` tillater at en varibel som f.eks. `x` kan listes opp sammen med tekststrenger fordi `print()` kan ta flere argumenter. Funksjonen `input()` kan derimot bare ta ett argument, så hvis du ønsker navnet på stoffet med i promptet for de neste input-setningene, må det plusses med annen tekst heller enn å listes opp med komma.
# 
# Hint 2:  Regn først ut antall mol ved å ta hvor mye stoff hun har i antall gram og dele på molvekten. Deretter multipliserer du antall mol med avogadros tall.

# ## b) Musikk

# Antall mulige melodilinjer på 10 toner (inkludert rytmevariasjoner) er anslått til å være 8.25 x 10<sup>19</sup>, jfr https://plus.maths.org/content/how-many-melodies-are-there. Lag et program i samme stil som 60m-programmet over som spør brukeren hvor mange ulike ti-toners melodilinjer hun selv tror hun har komponert og / eller hørt, og skriver ut som resultat hvor stor andel dette utgjør av antall mulige melodier (her vil dette sluttresultatet sannsynligvis bli et svært lite tall). 
# 
# Eksempel på kjøring:
# 
#   
# ```python
# Antall ulike 10-toners melodilinjer du har hørt? 3288
# Du har hørt 3.985454545454546e-15 prosent av melodier som er mulig.
# ```
# 
# ***Skriv koden din i blokka under.***

# In[17]:


estimat = int(input("Hvor mange ulike 10-toners melodier tror du at du har hørt? "))
print("Du har hørt", format(estimat/8.25e17, '.2e'), "prosent av alle mulige 10-toners melodier")


# #### Hint

# Ta antall ulike ti-toners melodilinjer du har hørt og divider på antall mulige melodilinjer på 10 toner og regn deretter tallet om til prosent.
