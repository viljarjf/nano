#!/usr/bin/env python
# coding: utf-8

# <nav class="navbar navbar-default">
#   <div class="container-fluid">
#     <div class="navbar-header">
#       <a class="navbar-brand" href="_Oving3.ipynb">Øving 3</a>
#     </div>
#     <ul class="nav navbar-nav">
#       <li ><a href="Intro%20til%20lokker.ipynb">Intro til løkker</a></li>
#     <li ><a href="Mer%20om%20lokker.ipynb">Mer om løkker</a></li>
#     <li><a href="Nostede%20lokker.ipynb">Intro til nøstede løkker</a></li>
#     <li ><a href="Kodeforstaelse.ipynb">Kodeforståelse</a></li>
#     <li ><a href="Gjett%20tallet.ipynb">Gjett tallet</a></li>
#        <li ><a href="Tekstbasert%20spill%202.ipynb">Tekstbasert spill 2</a></li>
#     <li ><a href="Geometrisk%20rekke.ipynb">Geometrisk rekke</a></li>
#     <li ><a href="Fibonacci.ipynb">Fibonacci</a></li>
#     <li><a href="Alternerende%20sum.ipynb">Alternerende sum</a></li>
#     <li ><a href="Hangman.ipynb">Hangman</a></li>
#     <li class="active"><a href="Doble%20lokker.ipynb">Doble løkker</a></li>
#     </ul>
#   </div>
# </nav>
# 
# # Doble løkker - til dels vanskelig
# 
# **Læringsmål:**
# 
# * Nøstede løkker
# 
# **Starting Out with Python:**
# 
# * Kap. 4.7

# a)  Skriv et program som benytter seg av en dobbel for-løkke og skriver ut følgende:
# 
# ```python
# 1
# 1 2
# 1 2 3
# 1 2 3 4
# 1 2 3 4 5
# ```
# 
# ***Skriv koden din her:***

# In[ ]:


def trekant(n):
    for x in range(n):
        l=[]
        for y in range(x+1):
            l.append(y+1)
        print(str(l).replace('[','').replace(']','').replace(',',''))
trekant(5)


# b) Skriv et program som benytter seg av en dobbel for-løkke og skriver ut følgende:
# 
# ```python
# X X
# X  X
# X   X
# X    X
# X     X
# ```
# 
# ***Skriv koden din her:***

# In[ ]:


for x in range(5):
    s='x '
    for y in range(x):
        s+=' '
    s+='x'
    print(s)


# **c)** Skriv et program som lar brukeren gi som input fra tastaturet et positivt heltall. Programmet skal da skrive ut primtallsfaktoriseringen til tallet, eller evt. at det allerede er et primtall. Eksempel på et par kjøringer:
# ```python
# Skriv inn et positivt heltall: 2
# 2 er et primtall
# >>>
# Skriv inn et positivt heltall: 38
# 38 = 2*19
# >>>
# Skriv inn et positivt heltall: 1000
# 1000 = 2*2*2*5*5*5
# >>>
# Skriv inn et positivt heltall: 73727
# 73727 er et primtall
# >>>
# Skriv inn et positivt heltall: 123456789
# 123456789 = 3*3*3607*3803
# >>>
# ```
# 
# Dette er et problem som peker i retning av dobbel løkke fordi samme tall kan være faktor flere ganger, som f.eks. i `1000  = 2*2*2*5*5*5`. Den ytre løkka trengs for å prøve ut stadig nye faktorer, den indre for å prøve om igjen samme faktor, i tilfelle den inngår flere ganger i tallet.
# 
# ***Skriv koden din her:***

# In[ ]:


tall=int(input('Skriv inn et positivt heltall '))
if tall==1 or tall==0:
    print('FY!')
tall_skjekk=tall
faktorer=[]
check=[2]
for x in range(2,tall):
    for y in check:
        if x%y==0:
            break
        else:
            if y==max(check):
                check.append(x)
    if x>=tall*0.5:
        break
for x in check:
    while tall%x==0:
        tall=tall//x
        faktorer.append(x)
for x in faktorer:
    tall*=x
if faktorer==[]:
    print(f'{tall} er et primtall')
elif tall==tall_skjekk:
    print(tall,'=',str(faktorer).replace('[','').replace(']','').replace(',','*'))


# **d)** Du skal hjelpe frøken Bernsen med å lage et enkelt program hvor elevene kan øve seg på den lille gangetabellen. Eleven skal stadig møte på nye gangestykker, og får 3 forsøk på hvert spørsmål. Benytt deg av randint(0,9) for å få tilfeldige tall for hvert gangestykke. Programmet skal fortsette frem til eleven gir beskjed om noe annet.
# 
# Eksempel på kjøring:
# 
# ```python
# Hva blir 2*0? 0
# Gratulerer, det er helt riktig!
# Er det ønskelig med flere spørsmål? Skriv 1 for ja og 0 for nei: 1
# >>> 
# Hva blir 8*6? 42
# Dessverre ikke riktig. Du har 2 forsøk igjen.
# Hva blir 8*6? 48
# Gratulerer, det er helt riktig!
# Er det ønskelig med flere spørsmål? Skriv 1 for ja og 0 for nei: 1
# >>>
# Hva blir 8*9? 73
# Dessverre ikke riktig. Du har 2 forsøk igjen.
# Hva blir 8*9? 74
# Dessverre ikke riktig. Du har 1 forsøk igjen.
# Hva blir 8*9? 78
# Dessverre ikke riktig. Du har 0 forsøk igjen.
# Dessverre klarte du ikke dette regnestykket, men vent så får du et nytt et:)
# Er det ønskelig med flere spørsmål? Skriv 1 for ja og 0 for nei: 1
# >>>
# Hva blir 9*1? 9
# Gratulerer, det er helt riktig!
# Er det ønskelig med flere spørsmål? Skriv 1 for ja og 0 for nei: 0
# >>>
# ```
# 
# ***Skriv koden din her:***

# In[6]:


import random
opg='1'
n=0
while opg=='1':
    a=random.randint(0,5*(int(n/5)+1))
    b=random.randint(0,5*(int(n/5)+1))
    for x in range(1,3):
        if int(input(f'Hva er {a}*{b}? '))==a*b:
            print('Riktig!')
            n+=1
            opg=input('Er det ønskelig med flere spørsmål? Skriv 1 for ja og 0 for nei: ')
            break
        else:
            print('Feil. Du har', 4-x, 'forsøk igjen')
            if x==4:
                print('Dessverre klarte du ikke dette regnestykket, men vent så får du et nytt et:)')
                n=0
                opg=input('Er det ønskelig med flere spørsmål? Skriv 1 for ja og 0 for nei: ')


# **e)** (frivillig)
# 
# Du skal endre programmet ditt fra d) slik at eleven først får veldig lette gangestykker ved å bruke randint(0,5) (fra random-biblioteket). Dersom eleven klarer å svare rett på 5 spørsmål på rad (eleven kan fremdeles bruke 3 forsøk), skal vanskelighetsgraden øke ved å bruke randint(0,10). Dette intervallet skal altså øke med 5 for hver gang eleven svarer korrekt på 5 spørsmål på rad. 
# 
# Eksempel på kjøring:
# 
# ```python
# Hva blir 1*2? 2                                                    #1 riktig svar
# Gratulerer, det er helt riktig!
# Er det ønskelig med flere spørsmål? Skriv 1 for ja og 0 for nei: 1
# ```
# ```python
# Hva blir 1*5? 5                                                    #2 riktige svar
# Gratulerer, det er helt riktig!
# Er det ønskelig med flere spørsmål? Skriv 1 for ja og 0 for nei: 1
#  ```
#  ```python
# Hva blir 3*5? 15                                                   #3 riktige svar
# Gratulerer, det er helt riktig!
# Er det ønskelig med flere spørsmål? Skriv 1 for ja og 0 for nei: 1
#  ```
#  ```python
# Hva blir 2*1? 2                                                    #4 riktige svar
# Gratulerer, det er helt riktig!
# Er det ønskelig med flere spørsmål? Skriv 1 for ja og 0 for nei: 1
#  ```
#  ```python
# Hva blir 2*0? 2
# Dessverre ikke riktig. Du har 2 forsøk igjen.
# Hva blir 2*0? 0                                                    #5 riktige svar
# Gratulerer, det er helt riktig!
# Er det ønskelig med flere spørsmål? Skriv 1 for ja og 0 for nei: 1
#  ```
#  ```python
# Hva blir 0*10? 0                                                    #Intervallet har økt og 1 riktig svar
# Gratulerer, det er helt riktig!
# Er det ønskelig med flere spørsmål? Skriv 1 for ja og 0 for nei: 1
# .
# .
# .
# Hva blir 15*29? 435                                                 
# Gratulerer, det er helt riktig!
# Er det ønskelig med flere spørsmål? Skriv 1 for ja og 0 for nei: 0
# ```
