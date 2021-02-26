#!/usr/bin/env python
# coding: utf-8

#  <nav class="navbar navbar-default">
#   <div class="container-fluid">
#     <div class="navbar-header">
#       <a class="navbar-brand" href="_Oving10.ipynb">Øving 10</a>
#     </div>
#     <ul class="nav navbar-nav">
#     <li ><a href="Rekursjon.ipynb">Rekursjon (Obligatorisk TDT4109)</a></li>
#     <li class="active"><a href="Matplotlib.ipynb">Matplotlib (Obligatorisk TDT4110)</a></li>
#     <li ><a href="Eksamen%202012.ipynb">Eksamen Python 2012</a></li>
#     <li ><a href="Sudoku.ipynb">Sudoku</a></li>
#     <li ><a href="numpy-arrays%20og%20matplotlib.ipynb">Numpy-arrays og matplotlib (TDT4110)</a></li>
#     <li ><a href="Bokanalyse%20med%20plotting.ipynb">Bokanalyse med plotting (TDT4110)</a></li>
#     <li ><a href="Sjakk.ipynb">Sjakk</a></li>
#     </ul>
#   </div>
# </nav>
# 
# 
# # Grunnleggende om plotting (Obligatorisk TDT4110)
# 
# **Læringsmål:**
# - Plotting

# ## Tutorial om plotting
# 
# Det kan være lurt å lese denne før du begynner på oppgaven under.

# For å tegne grafer er vi nødt til å bruke ekstrafunksjoner som er utenfor "standard python". Disse funksjonene er lagret i såkalte *bibliotek*, som er kode andre har laget og som vi kan bruke. Biblioteket vi skal bruke for å plotte grafer heter `matplotlib`.
# 
# Ofte er det ikke nødvendig å vite alt om hvordan et bibliotek fungerer, men heller hvordan man bruker det. Dette kan man finne ut av ved for eksempel å google eksempler på bruk (tutorials) eller lese dokumentasjonen for biblioteket. Den offisielle oversikten over matplotlib (fra de som har laget det) ligger for eksempel [her](https://matplotlib.org/3.1.1/contents.html). Denne inneholder informasjon om alt det er mulig å bruke matplotlib til (som er veldig mye!) og trengs ikke å leses for å kunne følge med videre i dette dokumentet.
# 
# ## Importering av matplotlib
# 
# For å kunne bruke biblioteket `matplotlib` må vi først *importere* det. I vårt tilfelle trenger vi ikke å importere hele matplotlib, men bare delen `pyplot` som er den delen som lar oss tegne grafer. Denne importerer vi i koden under og kaller for `plt`. Dette gjør at vi senere kun trenger å skrive `plt` i stedet for `matplotlib.pyplot`.

# In[4]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# `%matplotlib inline` gjør at grafene vises direkte i dokumentet. Uten denne vil du ikke kunne se grafene.
# 
# ## Nå: La oss tegne noen grafer! :D
# Under ser du et eksempel på en enkel kode som tegner en graf. Dette eksempelet består av tre kodelinjer som alle bruker `pyplot` fra `matplotlib`-biblioteket (som vi har døpt om til `plt`)
# 
# - Funksjonen `plt.plot` tar inn en liste med verdier som blir y-verdiene i grafen.
# - Funksjonen `plt.ylabel` brukes for å sette teksten som skal være på y-aksen.
# - Funksjonen `plt.show` brukes for å vise grafen
# 
# **Kjør koden under og se hva som skjer!** Prøv gjerne også å endre verdiene og kjøre koden på nytt

# In[ ]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

plt.plot([1, 2, 4, 3])
plt.ylabel('Noen tall')
plt.show()


# Det verdt å merke seg at listen som `plt.plot` tar inn også kan være en variabel. Dette er gjort i eksemepelet under. Her spørr vi brukeren om 4 tall og plotter disse tallene inn i en graf.
# 
# **Kjør koden under og se om du forstår hvordan den fungerer**

# In[ ]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

numbers = []
for x in range(4):
    number = int(input("Skriv inn et tall: "))
    numbers.append(number)

plt.plot(numbers)
plt.ylabel('Tallene du skrev inn')
plt.show()


# Det virker kanskje som om `plt.plot` ikke er så nyttig, siden alle punktene kun har 1 mellom seg på x-aksen. Dette er feil. Funksjonen har faktisk et hav av muligheter! Vi kan for eksempel spesifisere punkter både på x-aksen og y-aksen ved å gi inn to lister til funksjonen. I tillegg kan vi bruke funksjonen `plt.axis` for å bestemme hva som skal være startverdi og sluttverdi for aksene.
# 
# **Kjør koden under og prøv å endre verdiene for å se hva som skjer!** Prøv gjerne også å se hva som skjer hvis man har x-verdier som ikke er i stigende rekkefølge som nå.

# In[ ]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

x_verdier = [2,4,8,16]
y_verdier = [4,2,9,3]
plt.plot(x_verdier, y_verdier)
plt.axis([0, 20, 0, 15]) # x-aksen går her fra 0 til 20, mens y-aksen går fra 0 til 15
plt.show()


# Det er også mulig å lage punkter i stedet for linjer. Her må det legges med en streng i et spesielt format til `plt.plot`. I eksempelet under betyr strengen `"ro"` at vi bruker røde prikker. `r` for *red*, `o` for *runding*.
# 
# **Kjør koden under og se hva som skjer!** Prøv også å bytte ut `'ro'` med andre strenger, som `'g-'`, `'b^'`, `'r--'`, `'k:`' og `'ys'`

# In[ ]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

plt.plot([1, 2, 3, 4], [1, 4, 9, 16], 'ro')
plt.axis([0, 6, 0, 20])
plt.show()


# Dette gjør at vi også kan plotte flere grafer oppå hverandre og skille mellom de, som i eksempelet under:

# In[ ]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

plt.plot([0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5], 'r-')
plt.plot([0, 1, 2, 3, 4, 5], [0, 1, 4, 9, 16, 25], 'b-')
plt.axis([0, 6, 0, 26])
plt.show()


# # Oppgave: Plotting av sinus-funksjon

# I denne oppgaven skal du plotte en sinus-funksjon. Vi kan ikke plotte funksjonen direkte uten videre som vi ville gjort i geogebra, så vi må i stedet lage et stort antall punkter og plotte disse punktene. Vi gjør dette et steg av gangen.

# ## Oppgave a

# Lag en liste som heter `x_verdier` som inneholder alle verdiene fra og med `0.0` til og med `30.0` med et mellomrom på `0.1`. Print deretter ut x-verdiene. Har du gjort alt riktig skal utskriften være:
# 
# ```
# [0.0, 0.1, 0.2, ... 29.8, 29.9, 30.0]
# ```
# Listen skal altså inneholde 301 tall hvor ```...``` er resten av tallene.
# 
# 
# ***Skriv koden din under:***

# In[1]:


x_verdier=[x/10 for x in range(301)]
print(x_verdier)


# #### Hint:

# `range` i python fungerer ikke med desimaltall, så det kan være lurt å lage en tom liste for så å legge til elementer i lista ved hjelp av en løkke. 

# ## Oppgave b

# Nå skal du lage en ny liste som heter `y_verdier`. Denne skal inneholde `sin(x)` for alle x-verdiene i `x_verdier`. 
# 
# For å ta sinus av et tall kan du importere biblioteket `math`, for så å bruke funksjonen `math.sin` som her:
# ``` python
# import math
# math.sin(3) # Vil returnere sin(3), hvor 3 er en verdi i radianer
# ```
# 
# Når du har laget `y_verdier` printer du listen. Hvis du har gjort alt riktig skal utskriften være:
# ```
# [[0.0, 0.09983341664682815, 0.19866933079506122, ... -0.9989818049469494, -0.9984950306638146, -0.9880316240928618]
# ```
# Denne listen skal også ha en lengde på 301 tall. `...` er resten av tallene
# 
# ***Skriv koden din under:***

# In[3]:


import math
y_verdier=[math.sin(x) for x in x_verdier]
print(y_verdier)


# #### Hint:

# Det kan være lurt å starte med en ny tom liste for så å iterere gjennom listen du lagde i oppgave a med en løkke.

# ## Oppgave c

# Du skal nå plotte punktene du har definert i oppgave a og oppgave b. Grafen skal lages med `x_verdier` som x-verdier, `y_verdier` som y-verdier og være en rød linje. Hvis du lurer på hvordan du tegner grafer, les tutorial på toppen.
# 
# ***Skriv koden din under:***

# In[6]:


plt.plot(x_verdier, y_verdier)
plt.show()

