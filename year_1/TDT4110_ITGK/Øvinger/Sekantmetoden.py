#!/usr/bin/env python
# coding: utf-8

# <nav class="navbar navbar-default">
#   <div class="container-fluid">
#     <div class="navbar-header">
#       <a class="navbar-brand" href="_Oving5.ipynb">Øving 5</a>
#     </div>
#     <ul class="nav navbar-nav">
#     <li><a href="Grunnleggende%20om%20funksjoner.ipynb">Grunnleggende om funksjoner</a></li>
#     <li><a href="Varierte%20funksjoner.ipynb">Varierte funksjoner</a></li>
#     <li><a href="Lokale%20variabler.ipynb">Lokale variabler</a></li>
#     <li><a href="Globale%20variabler.ipynb">Globale variabler</a></li>
#     <li><a href="Euklids%20algoritme.ipynb">Euklids algoritme</a></li>
#     <li><a href="Primtall.ipynb">Primtall</a></li>
#     <li><a href="Multiplikasjon.ipynb">Multiplikasjon</a></li>
#         <li><a href="Den%20store%20sporreundersokelsen.ipynb">Den store spørreundersøkelsen</a></li>
#     <li><a href="Arbeidsdager.ipynb">Arbeidsdager</a></li>
#     <li class="active"><a href="Sekantmetoden.ipynb">Sekantmetoden</a></li>
#     <li><a href="Not%20quite%20Blackjack.ipynb">Not quite Blackjack</a></li>
#         <li><a href="Funksjoner%20og%20Jupyter%20widgets.ipynb">Funksjoner og Jupyter widgets</a></li>
#     </ul>
#   </div>
# </nav>
# 
# # Sekantmetoden
# 
# **Læringsmål:**
# - Funksjoner
# - Løkker
# 
# **Starting Out with Python:**
# - Kap. 4.2-4.3
# - Kap. 5.5
# - Kap. 5.8-5.9
# 
# I denne oppgaven skal vi implementere Sekantmetoden i Python.
# 
# Sekantmetoden kan benyttes for å finne nullpunkt til en matematisk funksjon. En matematisk funksjon har et nullpunkt der $f(x) = 0$, dvs. at grafen krysser x-aksen. 
# 
# Sekantmetoden er gitt ved:
# 
# $x_{k+1}=x_k-f(x_k)\frac{x_k-x_{k-1}}{f(x_k)-f(x_{k-1})}$
# 

# ## a)

# Lag en funksjon `f` som tar inn et tall `x` som argument og returnerer verdien til
# 
# $f(x)=(x-12)e^{x/2}-8(x+2)^{2}$
# 
# og en annen funksjon `g` som tar inn `x` som argument og returnerer verdien til
# 
# $g(x)=-x-2x^{2}-5x^{3}+6x^{4}$
# 
# ***Skriv koden din i kodeblokken under***

# In[3]:


import math
def f(x):
    return (x-12)*math.exp(x/2)-8*(x+2)**2
def g(x):
    return -x-2*x**2-5*x**3+6*x**4


# Test også koden din med et par verdier. Du kan for eksempel sjekke at `f(0)` returnerer `-44` og at `g(1)` returnerer `-2`.

# ## b)

# Sekantmetoden er en tilnærming av Newtons metode:
# 
# $x_{k+1}=x_{k}-\frac{f(x_{k})}{f'(x_{k})}$ hvor
# 
# $f'(x_k) \approx \frac{f(x_{k})- f(x_{k-1})}{x_{k}-x_{k-1}}$
# 
# Lag en funksjon `differentiate(x_k, x_k1, func)` som bruker formelen for den approksimerte (**f'(x)**) gitt i oppgaveteksten til å derivere. Funksjonen skal ta inn tre argumenter: `x_k`, `x_k1` og `func`, og returnere den deriverte (et flyttall):
# 
# - `x_k`: punktet hvor vi ønsker å finne den deriverte
# - `x_k1`: et tidligere punkt som vi bruker for å finne stigningstall
# - `func`: funksjonen man ønsker å derivere (i denne oppgaven vil `func` alltid tilsvare enten `f` eller `g` fra **a)**)
# 
# ***Skriv koden i kodeblokken under***

# In[5]:


def differentiate(x_k, x_k1, func):
    return (func(x_k)-func(x_k1))/(x_k-x_k1)


# For å teste funksjonen kan du kjør funksjonskallet `differentiate(9,10,f)`. dette skal returnere: -210.7749243035878

# ## c)

# Lag en funksjon `secant_method(x0, x1, func, tol)` som benytter seg av `differentiate(x_k, x_k1, func)` til å utføre sekantmetoden. Funksjonen skal returnere verdien(/avslutte) når endringen i `x` er mindre enn toleransegrensen `tol`. 
# 
# Test funksjonen din med følgende verdier:
# ```python
# secant_method(11,13,f,0.00001)
# secant_method(1,2,g,0.00001)
# secant_method(0,1,g,0.00001)
# ```
# 
# ***Skriv koden i kodeblokken under***

# In[58]:


def secant_method(x0, x1, func, tol):
    if abs(x1-x0)<tol:
        return x1
    x2 = x1-(func(x1)/differentiate(x0, x1, func))
    return secant_method(x1, x2, func, tol)


l=[secant_method(11,13,f,0.00001), secant_method(1,2,g,0.00001), secant_method(0,1,g,0.00001)]
for a in l:
    print('Funksjonen nærmer seg et nullpunkt i x=', round(a,2), 'der er funksjonsverdien', format([f,g,g][l.index(a)](a),'.2e'))


# **Eksempel på kjøring av kode:**
# ```python
# Funksjonen nærmer seg et nullpunkt når x = 13.92 , da er f(x) =  -1.59e-06
# Funksjonen nærmer seg et nullpunkt når x =  1.22 , da er f(x) =  -9.66e-08
# Funksjonen nærmer seg et nullpunkt når x =  0.0  , da er f(x) =  0.0
# ```

# #### Hint

# Som du kan se, trenger sekantmetoden to tidligere punkter for å finne et nytt. Pass på å skifte ut punktene etterhvert som det trengs.
