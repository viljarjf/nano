#!/usr/bin/env python
# coding: utf-8

# <nav class="navbar navbar-default">
#   <div class="container-fluid">
#     <div class="navbar-header">
#       <a class="navbar-brand" href="_Oving6.ipynb">Øving 6</a>
#     </div>
#     <ul class="nav navbar-nav">
#       <li ><a href="Generelt%20om%20lister.ipynb">Generelt om lister</a></li>
#     <li ><a href="Lett%20og%20blandet.ipynb">Lett og blandet</a></li>
#     <li ><a href="Kodeforstaelse.ipynb">Kodeforståelse</a></li>
#     <li ><a href="Vektorer.ipynb">Vektorer</a></li>
#     <li ><a href="Lister%20og%20lokker.ipynb">Lister og løkker</a></li>
#     <li ><a href="Teoridelen%20paa%20eksamen.ipynb">Teoridelen på eksamen</a></li>
#     <li ><a href="Gangetabell%20og%20lister.ipynb">Gangetabell og lister</a></li>
#     <li class="active"><a href="Lotto.ipynb">Lotto</a></li>
#     <li ><a href="Tannfeen.ipynb">Tannfeen</a></li>
#         <li><a href="Chattebot.ipynb">Chattebot</a></li>
#     <li ><a href="Matriseaddisjon.ipynb">Matriseaddisjon</a></li>
#     <li ><a href="Intro%20til%20numpy-arrays.ipynb">Intro til numpy-arrays</a></li>
#     </ul>
#   </div>
# </nav>
# 
# # Lotto
# 
# **Læringsmål:**
# 
# * Lister
# * Tilfeldige tall
# 
# **Starting Out with Python:**
# 
# * Kap. 7
# 
# I denne oppgaven lage du lage en lottosimulator. 
# 
# Reglene er som følger:
# 
# * Det trekkes ut 7 lottotall og 3 tilleggstall fra og med 1 til og med 34. Alle tallene som trekkes skal være unike.
# * Premier deles ut basert på følgende tabell:
# 
# Premiergruppe|Premie (kr)
# :---|---
# 7 rette	|2 749 455
# 6 rette + 1 tilleggstall	|102 110
# 6 rette	|3 385
# 5 rette	|95
# 4 rette + 1 tilleggstall	|45

# ### a)

# Lag en liste som heter `numbers` og som inneholder alle heltall fra og med 1 til og med 34.
# 
# ***Skriv koden din i boksen under.***

# In[1]:


numbers=range(1,35)


# ### b)

# Lag en liste som heter `myGuess` med 7 tall. Denne listen inneholder tallene som du tipper.
# 
# ***Skriv koden din i boksen under.***

# In[2]:


myGuess=[]
while len(myGuess)<7:
    r=int(input('Ditt tall: '))
    if r not in myGuess:
        myGuess.append(r)
print(myGuess)


# ### c) 

# Lag en funksjon som tar inn `n` som argument og som trekker ut `n` tall ut av listen `numbers` og legger de i en egen liste.  
# For å gjøre ting tilfeldig: `import random` og `random.randint(n,N)` gir tilfeldige tall fra og med n til og med N.
# 
# Eksempel på kjøring:
# 
# ```python
# >>>print(drawNumbers(numbers, 7))
# [16, 33, 5, 20, 7, 4, 8]
# ```
# 
# ***Skriv koden din i boksen under.***

# In[3]:


import random
def drawNumbers(liste, antall):
    r_l=[]
    while len(r_l)<antall:
        r=random.choice(liste)
        if r not in r_l:
            r_l.append(r)
    return r_l
choices=(drawNumbers(numbers, 7))
print(choices)


# #### Hint

# Hint: Bruk funksjonene `pop()` og `append()` for å fjerne og legge til elementer i en liste. Husk at pop fjerner et element i en indeks i lista, den fjerner ikke tallet. Så numbers.pop(rand_num) fjerner elementet på indeks rand_num - altså hvis rand_num er 13 fjernes tallet på indeks 13, ikke tallet 13!

# ### d)

# Lag funksjonen `compList` som sammenligner to lister med tall. Antall like tall i listene skal returneres.
# 
# Eksempel på kjøring:
# 
# ```python
# >>>print(compList(drawNumbers(numbers,7),myGuess))
# 1
# ```
# 
# ***Skriv koden din i boksen under.***

# In[4]:


def compList(liste_1, liste_2):
    l=[]
    for x in liste_1:
        if x in liste_2:
            l.append(x)
    return len(l)
compList(choices, myGuess)


# ### e)

# Lag en funksjon som tar inn antall like tall og like tilleggstall, og returnerer premien du har vunnet.
# 
# Eksempel på kjøring:
# 
# ```python
# >>>print(Winnings(7,1))
# 2749455
# >>>print(Winnings(5,2))
# 95
# >>>print(Winnings(3,1))
# 0
# ```
# 
# ***Skriv koden din i boksen under.***

# In[5]:


def winnings(tall, tillegg):
    if tall==4 and tillegg==1:
        return 45
    if tall==5:
        return 95
    if tall==6:
        return 3385
    if tall==6 and tillegg==1:
        return 102110
    if tall==7:
        return 2749455
    return 0


# ### f)

# Funksjonene skal settes sammen i main() slik at dette blir en fullverdig lottosimulator (for en lottorekke). Tallene du skal trekke ut (både lottotallene og tilleggstallene) kan legges i samme liste. Funksjonen `compList` kan da sammenligne de første 7 tallene, og så de siste 3 tallene, for å finne ut hvor mange like tall du har. main() skal returnere hvor mye du har tjent eller mest sannsynlig tapt på denne lottorekken. Dersom en lottorekke kosten 5 kroner, vil -5 returneres dersom Winnings() er 0. Hvis du er heldig og Winnings() blir 95 skal 90 returneres fra main(). 
# 
# **Husk at du kan bruke alle funksjoner du har definert over!**
# 
# ***Skriv koden din i boksen under.***

# In[6]:


def main():
    tall=drawNumbers(numbers,10)
    vinnertall=tall[:7]
    tilleggstall=tall[7:]
    return winnings(compList(vinnertall, myGuess),compList(tilleggstall, myGuess))
main()


# ### g) frivillig

# Finn ut hvor mye man har vunnet etter å ha tippet en million ganger. Anta at premiepotten er det samme hver uke, og at en lottorekke koster 5 kroner.
# 
# ***Skriv koden din i boksen under.***

# In[10]:


pængp=0
pængm=0
for x in range(1000000):
    pængm-=5
    pængp+=main()
print(pængm)
print(pængp)

