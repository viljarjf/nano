#!/usr/bin/env python
# coding: utf-8

# <nav class="navbar navbar-default">
#   <div class="container-fluid">
#     <div class="navbar-header">
#       <a class="navbar-brand" href="_Oving2.ipynb">Øving 2</a>
#     </div>
#     <ul class="nav navbar-nav">
#     <li><a href="Ulike%20typer%20if-setninger.ipynb">Ulike typer if-setninger</a></li>
#     <li><a href="Sammenligning%20av%20strenger.ipynb">Sammenligning av strenger</a></li>
#     <li><a href="Logiske%20operatorer%20og%20logiske%20uttrykk.ipynb">Logiske operatorer og logiske uttrykk</a></li>
#     <li><a href="Forbrytelse%20og%20straff.ipynb">Forbrytelse og straff</a></li>
#     <li ><a href="Aarstider.ipynb">Årstider</a></li>
#     <li class="active"><a href="Tekstbasert%20spill.ipynb">Tekstbasert spill</a></li>
#     <li><a href="Sjakkbrett.ipynb">Sjakkbrett</a></li>
#     <li><a href="Billettpriser%20og%20rabatter.ipynb">Billettpriser og rabatter</a></li>
#     <li><a href="Skatteetaten.ipynb">Skatteetaten</a></li>
#     <li><a href="Epletigging.ipynb">Datamaskinen som tigget epler</a></li>
#     <li><a href="Andregradsligning.ipynb">Andregradsligning</a></li>
#     </ul>
#   </div>
# </nav>
# 
# 
# # Tekstbasert spill
# 
# 
# **Læringsmål:**
# 
# - Betingelser
# 
# **Starting Out with Python:**
# 
# - Kap. 3.1- 3.2
# - Kap. 3.4
# 
# Noe gøy vi kan gjøre med if-setninger er å lage et enkelt tekstbasert spill. Her er et eksempel fra starten av et av de mest kjente tekstbaserte spillene, Zork:
# ```
# West of House
# This is an open field west of a white house, with a boarded front door.
# There is a small mailbox here.
# A rubber mat saying 'Welcome to Zork!' lies by the door.
# 
# >open mailbox
# You open the mailbox, revealing a small leaflet.
# 
# >read leaflet
# (first taking the small leaflet)
#                           WELCOME TO ZORK
# 
#     ZORK is a game of adventure, danger, and low cunning.  In it you will explore some of the most amazing territory ever seen by mortal man.  Hardened adventurers have run screaming from the terrors contained within!
#     ...
#     ```
#     
# Som du ser gjør man kommandoer i spillet ved å skrive inn hva man ønsker å gjøre. Da må man passe på at programmet klarer å kjenne igjen flere kommandoer en bruker kan tenke å skrive inn.

# ### a)

# Skriv en intro til spillet ditt på en eller to setninger. La så brukeren skrive inn hva den ønsker å gjøre, og lag feedback for minst tre forskjellige muligheter ved hjelp av if-setninger. (Ønsker brukeren å åpne en dør, hva skjer? Ønsker brukeren å løpe vekk, hva skjer? Se på Zork eksempelet over eller test det ut selv [her](http://zorkonline.net/) om du trenger inspirasjon.) Husk å skriv kode for minst tre forskjellige scenarioer. I denne deloppgaven trenger du ikke ta hensyn til om brukeren skrev inn noe annet enn du forventet.
# 
# Eksempel:
# ```python
# Du står utenfor en dør.
# >gå inn
# Døren er låst.
# 
# Du står utenfor en dør.
# >bank på
# Ingen svarer
# 
# Du står utenfor en dør.
# >lås opp
# Du låser opp døren
# ```
# 
# ***Skriv koden din her:***

# In[26]:


x = input("Du står ovenfor en dør. ").lower()
if x=='gå inn' or x=='gå inn døra':
    print('Døren er låst.')
elif x=='bank på' or x=='bank på døra' or x=='banker på':
    print('Ingen svarer')
elif x=='lås opp' or x=='låser opp' or x=='låser opp døra':
    print('Du låser opp døren')
else:
    print('Dette er ikke en støttet kommando')


# ### b)

# I visse tilfeller vil brukeren skrive inn noe annet enn vi forventer. Ta hensyn til dette i spillet ved å si 
# i fra dersom noe brukeren skriver ikke støttes.
# 
# Eksempel: 
# ```python
# Du står utenfor en dør.
# >gå inn
# Døren er låst.
# 
# Du står utenfor en dør.
# >bank på
# Ingen svarer
# 
# Du står utenfor en dør.
# >løp og gjem deg
# Dette er ikke en støttet kommando
# ```
# 
# ***Skriv koden i samme blokk som oppgave a***

# ### c)

# Endre spillet så det ikke spiller noen rolle om brukeren skriver inn store eller små bokstaver i kommandoen sin.
# 
# Eksempel:
# ```python
# Du står utenfor en dør.
# >gå inn
# Døren er låst.
# 
# Du står utenfor en dør.
# >Gå Inn
# Døren er låst.
# ```
# ***Skriv koden i samme blokk som oppgave a***

# ### d)

# Ofte når vi driver med denne slags kommandoer vil det være nesten like formuleringer som betyr det samme, men siden vi nå programmerer må svaret være eksakt det samme som vi forventer. **For hvert scenario, ta hensyn til at brukeren kan formulere kommandoen på minst to måter.**
# 
# Eksempel:
# ```python
# #scenario 1
# Du står utenfor en dør.
# >gå inn
# Døren er låst.
# 
# Du står utenfor en dør.
# >gå inn døra
# Døren er låst.
# 
# #scenario 2
# Du står utenfor en dør.
# >bank på
# Ingen svarer
# 
# Du står utenfor en dør.
# >banker på
# Ingen svarer
# ```
# 
# ***Skriv koden i samme blokk som oppgave a***
