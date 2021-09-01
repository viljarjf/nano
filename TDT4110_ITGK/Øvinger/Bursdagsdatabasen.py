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
#     <li class="active"><a href="Bursdagsdatabasen.ipynb">Bursdagsdatabasen</a></li>
#     <li ><a href="Tallak%20teller%20antall%20tall.ipynb">Tallak teller antall tall</a></li>
#     <li ><a href="Opptaksgrenser.ipynb">Opptaksgrenser</a></li>
#         <li ><a href="Soke%20i%20tekst.ipynb">Søke i tekst</a></li>
#     <li ><a href="Tre%20paa%20rad.ipynb">Tre på rad</a></li>
#     </ul>
#   </div>
# </nav>
# 
# # Bursdagsdatabasen
# 
# **Læringsmål:**
# 
# * Dictionaries
# * Exceptions
# 
# **Starting Out with Python:**
# 
# * Kap. 9.1 Dictionaries
# * Kap. 6.8 Exceptions
# 
# I denne oppgaven skal du lage en metode for å oppdatere en dictionary (**birthdays**) bestående av datoer og navn. Dette må du gjøre ved å benytte deg av unntakshåndtering(exceptions). 
# 
# Vemund, som er en smule glemsk når det gjelder bursdager, ønsker å lage en stor database med bursdagene til alle vennene sine.
# 
# For å skaffe seg et godt utgangspunkt har han etterspurt og fått tilsendt følgende database (i form av en python-dictionary) fra IDIs seksjon for “data and information management”, som har det statlige ansvaret for lagring av bursdager.
# 

# In[11]:


birthdays = {
"22 nov": ["Bob Bernt", "Mathias"],
"20 mar": "Simen",
"31 okt": ["Aragusta", "Carina"],
"12 jan": "Silje",
"3 sep": "Tobias",
"5 jul": ["Martin", "Øystein"],
"11 mar": "Miriam"
}


# Databasen består av datonøkler(**string**) som peker til enten et navn(**string**) eller en **liste** med navn til personer som har bursdag den datoen.
# 
# Dessverre er ikke denne databasen særlig komplett, så Vemund ønsker å legge til nye bursdager etter hvert som han får nye venner.
# 
# Han har laget følgende funksjon for å gjøre dette:

# In[10]:


def add_birthday_to_date(date, name):
    try:
        birthdays[date].append(name)
    except AttributeError:
        birthdays[date]=[birthdays[date], name]
    except KeyError:
        birthdays[date]=name


# Som f.eks. kan kalles slik:

# In[3]:


add_birthday_to_date("31 okt", "Gunnar")


# Vemund møter derimot på et problem når han prøver å legge til et bursdagsbarn på datoer som ikke finnes, eller bare har ett bursdagsbarn fra før.
# 
# Istedet for at funksjonen gjør som den skal, grynter den og spytter tilbake to forskjellige exceptions (unntak) til Vemund. Prøv å kjør kodesnuttene selv, og se hva som skjer. Husk å kjør kodesnuttene som definerer databasen og funksjonen først.

# In[4]:


add_birthday_to_date ("12 jan", "Sindre")


# In[ ]:


add_birthday_to_date ("9 feb", "Lillian")


# Den første feilen kommer av at verdien tilsvarende nøkkelen “12 jan” ikke er en liste, men en enkel streng.
# 
# Den andre feilen kommer av at nøkkelen “9 feb” ikke finnes i databasen.
# 
# Vemund ønsker at funksjonen tar hensyn til disse grensetilfellene.
# 
# **Oppgave:** Løs disse problemene ved hjelp av Python sin støtte for unntakshåndtering der du benytter setningene try og except.

# ### Generelt om exceptions

# Dersom du ønsker å spørre brukeren om å skrive inn et heltall, kan det være ønskelig å lage variabelen slik: a = int(input("Skriv et tall: ")), men dette kan misforstås av brukeren. Brukeren svarer kanskje "fjorten", altså 14 skrevet med bokstaver. Ettersom du har brukt int() i variabelen a slik at brukerens input skal bli konvertert til et heltall, vil det komme en feilmelding. Prøv å skrive et tall med tekst i eksempelt under.

# In[ ]:


a = int(input("Skriv et tall:"))


# Eller la oss si at du ønsker å ta inn to tall og dele det første tallet på det andre tallet. Dersom det andre tallet er null vil du også få en feilmelding. Prøv selv under.

# In[ ]:


a=10
b=int(input("Skriv et tall:"))
print(a/b)


# En elegant metode å håndtere disse feilmeldingene på er ved å bruke try og exceptions. Det kan minne en del om if/else bare at try/except kan håndtere flere ting og du trenger ikke å spesifisere noen betingelse. Alt du ønsker å utføre i koden skal skrives under try. except kjøres kun dersom noe går galt under try.

# In[ ]:


try:
    a = int(input('Skriv et tall: '))
    b = int(input('Skriv et tall: '))
    print(a/b)
except:
    print('Noe har gått galt! Har du husket at det er umulig å dele på null'
          'eller at du skulle skrive inn et heltall her?')


# Dersom brukeren skriver inn noe annet enn et heltall eller skriver at det andre tallet er null, blir det under except printet. Denne feilmeldingen kan være litt forvirrende for brukeren ettersom han eller hun ikke vet hva som gikk galt. Var det at det ble delt på null eller at noe annet enn et heltall ble skrevet inn? For å gjøre det klarere kan man dele inn except i ulike punkter som håndterer ulike feil. Som man kan se i det første bildet over kom det en feilmelding kalt "ValueError", og på bildet under kom det en feilmelding kalt "ZeroDivisionError", la oss bruke disse:

# In[ ]:


try:
    a = int(input('Skriv et tall: '))
    b = int(input('Skriv et tall: '))
    print(a/b)
except ValueError:
    print('Husket du å skrive inn et heltall her?')
except ZeroDivisionError:
    print("Husk at du ikke kan dele på null")


# Nå vil brukeren få en mer forklarende feilmeldinger. Prøv selv!

# ### a)

# Legg til funksjonalitet til funksjonen `add_birthday_to_date(date, name)` slik at det opprettes en liste med flere personer, dersom flere har bursdag på samme dag. **Du kan fortsette på funksjonen skrevet over i oppgaven.**

# #### Hint

# Dette hindrer en AttributeError.

# ### b)

# Legg til funksjonalitet til funksjonen `add_birthday_to_date(date, name)` slik at det er mulig å legge til nye bursdager på nye datoer i dictionarien. **Du kan fortsette på funksjonen skrevet over i oppgaven.**

# #### Hint

# Dette hindrer en KeyError.

# ### Testkode:

# Du kan teste at unntakshåndteringen fungerer ved å kjøre de samme to grensetilfellene som tidligere:

# In[13]:


add_birthday_to_date("12 jan", "Sindre")
add_birthday_to_date("9 feb", "Lillian")


# Dette skal nå oppdatere databasen uten feilmeldinger. 
# 
# Utskrift av birthdays etter kjøring av "Testkode" skal gi:
# 
# ```python
# {'22 nov': ['Bob Bernt', 'Mathias'], '20 mar': 'Simen, '31 okt': ['Aragusta', 'Carina'], '12 jan': ['Silje', 'Sindre'], '3 sep': 'Tobias', '5 jul': ['Martin', 'Øystein'], '11 mar': 'Miriam', '9 feb': 'Lillian'}
# ```
# 
# Sjekk selv med koden under.

# In[14]:


print(birthdays)

