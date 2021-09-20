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
#         <li ><a href="Tekstbasert%20spill%202.ipynb">Tekstbasert spill 2</a></li>
#     <li ><a href="Geometrisk%20rekke.ipynb">Geometrisk rekke</a></li>
#     <li class="active"><a href="Fibonacci.ipynb">Fibonacci</a></li>
#     <li><a href="Alternerende%20sum.ipynb">Alternerende sum</a></li>
#     <li ><a href="Hangman.ipynb">Hangman</a></li>
#     <li ><a href="Doble%20lokker.ipynb">Doble løkker</a></li>
#     </ul>
#   </div>
# </nav>
# 
# # Fibonacci
# 
# **Læringsmål:**
# 
# * Løkker
# 
# **Starting Out with Python:**
# 
# * Kap. 4.3
# 
# <br><br>
# I denne oppgaven skal du bruke løkker til å regne ut fibonaccitall.  
# 
# Fibonaccitallene er definert som følger: 
# 
# * **f(0)=0**
# * **f(1)=1**
# * **f(k)=f(k−1)+f(k−2)**
# 
# Det vil si at de to første tallene i rekken er 0 og 1, deretter er det neste tallet summen av de to forrige tallene. Starten på rekken ser derfor slik ut: 0 1 1 2 3 5 8 13 ...

# **a)** Lag et program som regner ut og returnerer det k-te fibonaccitallet f(k) ved hjelp av iterasjon. Har du gjort det rett skal det 10-ende Fibonaccitallet bli 55. **Husk at det første tallet i rekken er tall nummer 0**
# 
# ***Skriv koden din her:***

# In[4]:


def fiboaocci(k):
    l=[0,1]
    for x in range(k-1):
        l.append(l[x]+l[x+1])
    print('Tall:',l[k])
    print('Sum:',sum(l))
    print('\n',l)
fiboaocci(10)


# **b)** Skriv om programmet i deloppgave a) slik at det også regner ut summen av alle fibonaccitallene. Har du gjort det rett det rett skal summen av Fibonaccitallene opp til 10 bli 143.

# **c)** (**Frivillig**, vanskeligere oppgave) Modifiser programmet til å returnere en liste med alle fibonaccitallene opp til og med f(k).
# 
# Husk å skrive ut svarene til skjerm.
