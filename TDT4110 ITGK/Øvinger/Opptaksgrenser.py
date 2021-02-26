#!/usr/bin/env python
# coding: utf-8

# <nav class="navbar navbar-default">
#   <div class="container-fluid">
#     <div class="navbar-header">
#       <a class="navbar-brand" href="_Oving9.ipynb">Øving 9</a>
#     </div>
#     <ul class="nav navbar-nav">
#     <li ><a href="Generelt%20om%20dictionary.ipynb">Generelt om dictionary</a></li>
#     <li ><a href="Innebygde%20funksjoner%20i%20dictionaries.ipynb">Innebygde funksjoner</a></li>
#     <li ><a href="Generelt%20om%20sets.ipynb">Generelt om sets</a></li>
#     <li ><a href="Generelt%20om%20filbehandling.ipynb">Generelt om filbehandling</a></li>
#     <li ><a href="Osteviruset.ipynb">Osteviruset</a></li>
#     <li ><a href="Bursdagsdatabasen.ipynb">Bursdagsdatabasen</a></li>
#     <li ><a href="Tallak%20teller%20antall%20tall.ipynb">Tallak teller antall tall</a></li>
#     <li class="active"><a href="Opptaksgrenser.ipynb">Opptaksgrenser</a></li>
#         <li ><a href="Soke%20i%20tekst.ipynb">Søke i tekst</a></li>
#     <li ><a href="Tre%20paa%20rad.ipynb">Tre på rad</a></li>
#     </ul>
#   </div>
# </nav>
# 
# 
# # Opptaksgrenser
# 
# **Læringsmål:**
# 
# * Lese fra filer
# * dictionaries
# 
# **Starting Out with Python:**
# 
# * Kap. 6: Files and Exceptions
# * Kap. 9.1 Dictionaries
# 
# I denne oppgaven skal vi lese inn en fil med opptaksgrensene fra Samordna Opptak.
# 
# Filen er på CSV-format (Comma Separated Values), noe som betyr at hver linje er en liste med felter separert med komma. Tekstfelter er omsluttet av fnutter (").
# 
# * Første felt er studiets navn
# * Andre felt er poenggrensen (enten et tall, eller "Alle" dersom alle kom inn)
# 
# F.eks. linjen: **"NTNU 194459 Antikkens kultur","Alle"** sier at alle som søkte kom inn på Dragvoll-studiet “Antikkens kultur” ved NTNU.
# 
# Hver funksjon i de følgende deloppgavene tar data fra filen **poenggrenser_2011.csv** som input. Derfor er det veldig praktisk å lagre innholdet i en variabel, slik at du slipper å lese den på nytt hver gang.

# ### a)

# Les fra fila `poenggrenser_2011.csv` og lagre innholdet i en variabel.
# 
# ***Skriv koden din i boksen under.***

# In[1]:


fil=open('poenggrenser_2011.csv', 'r')
temp=fil.read().replace('"', '').split('\n')
poenggrenser=[]
for i in temp:
    poenggrenser.append(i.split(','))
poenggrenser=poenggrenser[:-1]
for x in poenggrenser:
    print(x)
print('\n\n\n\n\n\~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n\n\n\n')

# ### b)

# Skriv en funksjon som finner ut hvor mange studier som tok inn alle søkere. 
# 
# ***Husk at du nå i alle deloppgavene kan bruke variabelen du definerte i a så lenge du har kjørt den kodesnutten først!***
# 
# *Eksempel på kjøring av kode:*
# ```python
# Antall studier hvor alle kom inn: 590
# ```
# ***Skriv koden din i boksen under.***

# In[2]:


def antall_studier_med_alle():
    n=0
    for i in poenggrenser:
        if i[1]=='Alle':
            n+=1
    return n
print('studier alle kommer inn', antall_studier_med_alle()


# ### b)

# Skriv en funksjon som finner gjennomsnittlig opptaksgrense for NTNU. Ikke ta med studier som tok inn alle søkere.
# 
# *Eksempel på kjøring av kode:*
# ```python
# Gjennomsnittlig opptaksgrense for NTNU var: 46.29
# ```
# ***Skriv koden din i boksen under.***

# In[6]:


def avg_snitt(skole):
    n=[]
    for i in poenggrenser:
        if skole in i[0]:
            if i[1]!='Alle':
                n.append(float(i[1]))
    return round(sum(n)/len(n), 2)

print(avg_snitt('NTNU'), 'NTNU')
print(avg_snitt('UIO'), 'UIO')
print(avg_snitt('HIB'), 'HIB')


# #### Hint

# For å sjekke om studiet var på NTNU kan du hente ut de fire første bokstavene i hver linje. Hvis du har en string studie kan du gjøre dette ved å skrive: studie[1:5]

# ### c)

# Skriv en funksjon som finner studiet med laveste opptaksgrense (som IKKE tok inn alle søkere).
# 
# *Eksempel på kjøring av kode:*
# ```python
# Studiet som hadde den laveste opptaksgrensen var: AHO 189343 Industridesign
# ```
# ***Skriv koden din i boksen under.***

# In[14]:


def find_min_snitt():
    n=100
    res=[]
    for i in poenggrenser:
        if i[1]!='Alle':
            if float(i[1])<n:
                n=float(i[1])
                res=i
    return res

def find_max_snitt():
    n=0
    res=[]
    for i in poenggrenser:
        if i[1]!='Alle':
            if float(i[1])>n:
                n=float(i[1])
                res=i
    return res

print('minste snitt', find_min_snitt())
print('største snitt', find_max_snitt())


# ### d)

# Lag en dictionary som har studiestedet som nøkkel og en liste med dictionaries som verdi. Denne listen med dictionaries skal ha navnet på linjen som nøkkel og opptakspoengene til den tilsvarende linjen som verdi. Dersom en linje har navnet "Fysikk og Matematikk" trenger du kun å ta hensyn til det første ordet, dvs. "Fysikk". 
# 
# **Eksempel på utskrift:**
# 
# ```python
# ATH [{'Kristendom': ' Alle'}, {'Interkulturell': ' Alle'}, {'Musikk': ' Alle'}, {'Teologi': ' Alle'}, {'Kristendom': ' Alle'}, {'Psykologi': ' Alle'}, {'Musikk': ' Alle'}, {'Interkulturell': ' Alle'}, {'Psykologi': ' Alle'}, {'Praktisk': ' Alle'}]
# AHO [{'Arkitekt': '12.3'}, {'Industridesign': '11.7'}]
# BDH [{'Sykepleierutdanning': '45.5'}]
# MF [{'Kristendom/RLE': ' Alle'}, {'Samfunnsfag': ' Alle'}, {'Interkulturell': ' Alle'}, {'Teologi': ' Alle'}, {'Religion': ' Alle'}, {'Ungdom': ' Alle'}, {'Lektor-': ' Alle'}, {'Teologi': ' Alle'}]
# DHS [{'Sykepleierutdanning': '48.3'}, {'Vernepleierutdanning': '41.8'}, {'Sosialt': '49.1'}, {'Sosialt': '42.4'}, {'Ergoterapeututdanning': '32.6'}]
# DMMH [{'Førskolelærerutdanning': '36.3'}, {'Førskolelærer': '39.1'}, {'Førskolelærer': '44'}, {'Førskolelærer': '46.2'}, {'Førskolelærer': ' Alle'}]
# .
# .
# .
# UIT [{'Ingeniør': ' Alle'}, {'Ingeniør': ' Alle'}, {'Ingeniør': ' Alle'}, {'Ingeniør': ' Alle'}, {'Sykepleierutdanning': '43.8'}, {'Lærerutdanning': ' Alle'}, {'Lærerutdanning': ' Alle'}, {'Førskolelærerutdanning': ' Alle'}, ....
# ```
# ***Skriv koden din i boksen under.***

# In[42]:


studier={}
keys=[]
keydict=[]
for i in poenggrenser:
    if i[0][:i[0].index(' ')] not in keys:
        keys.append(i[0][:i[0].index(' ')])
for key in keys:
    temp_key_list=[]
    for i in poenggrenser:
        if i[0][:i[0].index(' ')]==key:
            short_key_name=i[0][i[0].index(' ')+1:]

            short_key_name=short_key_name[short_key_name.index(' ')+1:]

            if ' ' in short_key_name:
                short_key_name=short_key_name[:short_key_name.index(' ')]

            temp_key_list.append({short_key_name :i[1]})
    studier[key]=temp_key_list
#print(studier)

