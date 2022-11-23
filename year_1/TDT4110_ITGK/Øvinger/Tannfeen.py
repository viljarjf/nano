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
#     <li ><a href="Lotto.ipynb">Lotto</a></li>
#     <li class="active"><a href="Tannfeen.ipynb">Tannfeen</a></li>
#         <li><a href="Chattebot.ipynb">Chattebot</a></li>
#     <li ><a href="Matriseaddisjon.ipynb">Matriseaddisjon</a></li>
#     <li ><a href="Intro%20til%20numpy-arrays.ipynb">Intro til numpy-arrays</a></li>
#     </ul>
#   </div>
# </nav>
# 
# # Tannfeen
# 
# **Læringsmål:**
# 
# * Lister
# * Løkker
# 
# **Starting Out with Python:**
# 
# * Kap. 7.8
#  
# 
# *Overformynderiet for tannfeer og python-programmerere* har vedtatt at istedenfor å betale 20 kroner for hver enkelt tann et barn mister og putter i vannglasset sitt, er de nå nødt til å betale per gram tann. Det ble bestemt at ett gram tann er verd 1 krone. Tannfeer vil helst bruke så store mynter de kan (i verdi). Gyldige mynter er [20,10,5,1].
# 
# Siden tannfeen besøker så mange, vil de ha et program som skal kunne regne ut dette fra lister. Det vil si at programmet tar inn en liste av tannvekter, og får tilbake en liste (av lister) over hvilke mynter som trengs for tennene.
# 
# Eksempel:
# 
# ```python
# teeth = [53,28]
# Skal gi ut
# [[2,1,0,3],[1,0,1,3]]```
# 
# Eksempelet over vil si at for 53g vil man få 2 stk 20kr, 1 stk 10kr, 0 stk 5kr og 3 stk 1kr, og for 28g vil man få 1 stk 20kr, 0 stk 10kr, 1 stk 5kr og 3 stk 1kr.
# 
# **Oppgave:** Lag programmet og test med listen under.

# In[38]:


teeth = [95,103,71,99,114,64,95,53,97,114,109,11,2,21,45,2,26,81,54,14,118,108,117,27,115,43,70,58,107]


# In[68]:


#skriv koden din her
teeth= [95,103,71,99,114,64,95,53,97,114,109,11,2,21,45,2,26,81,54,14,118,108,117,27,115,43,70,58,107]
pæng=[20,10,5,1]
ferdig=[]
teeth_check=teeth
for x in range(len(teeth_check)):
    l=[0,0,0,0]
    for i in range(len(l)):
        while teeth_check[x]-pæng[i]>=0:
            l[i]=l[i]+1
            teeth_check[x]=teeth_check[x]-pæng[i]
    ferdig.append(l)
for x in ferdig:
    print(f'20: {x[0]}, 10: {x[1]}, 5: {x[2]}, 1: {x[3]}')
        


# Dersom du skrevet koden riktig skal listen over gi følgende utskrift:
# 
# ```python
# [[4, 1, 1, 0], [5, 0, 0, 3], [3, 1, 0, 1], [4, 1, 1, 4], [5, 1, 0, 4], [3, 0, 0, 4],  
# [4, 1, 1, 0], [2, 1, 0, 3], [4, 1, 1, 2], [5, 1, 0, 4], [5, 0, 1, 4], [0, 1, 0, 1],  
# [0, 0, 0, 2], [1, 0, 0, 1], [2, 0, 1, 0], [0, 0, 0, 2], [1, 0, 1, 1], [4, 0, 0, 1],  
# [2, 1, 0, 4], [0, 1, 0, 4], [5, 1, 1, 3], [5, 0, 1, 3], [5, 1, 1, 2], [1, 0, 1, 2],  
# [5, 1, 1, 0], [2, 0, 0, 3], [3, 1, 0, 0], [2, 1, 1, 3], [5, 0, 1, 2]]
# ```
# På penere form:
# ```python
# 20: 4 , 10: 1 , 5: 1 , 1: 0
# 20: 5 , 10: 0 , 5: 0 , 1: 3
# 20: 3 , 10: 1 , 5: 0 , 1: 1
# 20: 4 , 10: 1 , 5: 1 , 1: 4
# 20: 5 , 10: 1 , 5: 0 , 1: 4
# 20: 3 , 10: 0 , 5: 0 , 1: 4
# 20: 4 , 10: 1 , 5: 1 , 1: 0
# 20: 2 , 10: 1 , 5: 0 , 1: 3
# 20: 4 , 10: 1 , 5: 1 , 1: 2
# 20: 5 , 10: 1 , 5: 0 , 1: 4
# 20: 5 , 10: 0 , 5: 1 , 1: 4
# 20: 0 , 10: 1 , 5: 0 , 1: 1
# 20: 0 , 10: 0 , 5: 0 , 1: 2
# 20: 1 , 10: 0 , 5: 0 , 1: 1
# 20: 2 , 10: 0 , 5: 1 , 1: 0
# 20: 0 , 10: 0 , 5: 0 , 1: 2
# 20: 1 , 10: 0 , 5: 1 , 1: 1
# 20: 4 , 10: 0 , 5: 0 , 1: 1
# 20: 2 , 10: 1 , 5: 0 , 1: 4
# 20: 0 , 10: 1 , 5: 0 , 1: 4
# 20: 5 , 10: 1 , 5: 1 , 1: 3
# 20: 5 , 10: 0 , 5: 1 , 1: 3
# 20: 5 , 10: 1 , 5: 1 , 1: 2
# 20: 1 , 10: 0 , 5: 1 , 1: 2
# 20: 5 , 10: 1 , 5: 1 , 1: 0
# 20: 2 , 10: 0 , 5: 0 , 1: 3
# 20: 3 , 10: 1 , 5: 0 , 1: 0
# 20: 2 , 10: 1 , 5: 1 , 1: 3
# 20: 5 , 10: 0 , 5: 1 , 1: 2
# ```
