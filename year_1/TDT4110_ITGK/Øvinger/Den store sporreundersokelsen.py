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
#     <li class="active"><a href="Den%20store%20sporreundersokelsen.ipynb">Den store spørreundersøkelsen</a></li>
#     <li><a href="Arbeidsdager.ipynb">Arbeidsdager</a></li>
#     <li><a href="Sekantmetoden.ipynb">Sekantmetoden</a></li>
#     <li><a href="Not%20quite%20Blackjack.ipynb">Not quite Blackjack</a></li>
#         <li><a href="Funksjoner%20og%20Jupyter%20widgets.ipynb">Funksjoner og Jupyter widgets</a></li>
#     </ul>
#   </div>
# </nav>
# 
# ## Den store spørreundersøkelsen
# 
# **Læringsmål:**
# 
# * Funksjoner 
# * Betingelser
# * Løkker
# 
# **Starting Out with Python:**
# 
# * Kap. 3.1-3.2
#  * 3.1: The if Statement
#  * 3.2: The if-else Statement 
# * Kap. 4.2
#  * 4.2: The while Loop: A Condition-Controlled Loop
# * Kap. 5.4-5.6, 5.8 
#  * 5.4: Local Variables
#  * 5.5: Passing Arguments to Functions
#  * 5.6: Global Variables and Global Constants
#  * 5.8: Writing Your Own Value-Returning Functions
#  
# 
# **I denne oppgaven skal du skrive et større program. For denne typen oppgaver kan det være mer praktisk å laste ned python og eventuelt en IDE (Et område man programmerer i på sin egen maskin). Ta derfor en kikk [her](https://docs.google.com/document/d/17tS0maWyzORUsIjmCVEszfqrl2X4By-Cy2Sw3ENG5lA/edit?usp=sharing) før du begynner. Det er fortsatt mulig å gjøre oppgaven i Jupyter dersom du ikke ønsker å jobbe lokalt**
#  
# I denne oppgaven skal du implementere et lite utdrag av en spørreundersøkelse om leksevaner til studenter. Undersøkelsen er beregnet for kvinner og menn i aldersgruppen 16-25 år.
# 
# Spørreundersøkelsen implementeres ved hjelp av å skrive ut spørsmål og lese input fra brukeren i en while-løkke som kjøres så lenge brukeren ønsker å skrive inn data. Når alle spørsmålene er besvart, gjentas spørsmålene for en ny person. 
# 
# Hold styr på fem globale tellere (variabler) under kjøringen av while-løkken: **antall_kvinner**, **antall_menn**, **antall_fag**, **antall_ITGK**, og **antall_timer_lekser**. Hvis brukeren til enhver tid svarer hade på et spørsmål skal while-løkken avsluttes og verdiene av de fem tellerne skrives ut.
# 
# I programmet ditt kan du få bruk for:

# In[ ]:


from sys import exit        #Du kan nå bruke funksjonen exit() i programmet ditt. Anbefales brukt i sjekk_svar-funksjonen.


# exit() vil avslutte kjøringen av programmet.
# 
# Bruk funksjoner til å lese inn svar fra brukeren (de bør være forskjellige om brukeren skriver inn et tall eller en streng), og til å skrive ut statistikk til slutt (oppgave g).
# 
# Funksjoner som kan implementeres i løpet av oppgaven er:
# 
# sjekk_svar(spm)
# les_streng(spm)
# les_ja_nei(spm)
# les_tall(spm)
# skriv_statistikk()
# (Der spm er svaret på de forskjellige spørsmålene som skal stilles i while-løkken)
# 
# Deloppgave a til e skal altså implementeres inni while-løkken.

# In[1]:


from sys import exit
menn=0
kvinner=0
alder=0
virkelig=''
fag=0
ITGK=0
lekser=[]

def ny_input(tekst):
    global loop
    svar=input(tekst)
    if svar=='hade':
        exit()
    return svar

def kjønn_skjekk(svar):
    global kvinner
    global menn
    if svar=='f':
        kvinner+=1
    elif svar=='m':
        menn+=1
    else:
        return 0
    return 1

def alder_skjekk(svar):
    global alder
    global virkelig
    virkelig=''
    try:
        svar=int(svar)
        if svar>=16 and svar<=25:
            if svar>22:
                virkelig='virkelig ' 
        else:
            print('Da kan du ikke ta denne undersøkelsen')
            alder=1
        return 1
    except:
        return 0

def fag_skjekk(svar):
    global fag
    if svar=='ja':
        fag+=1
    elif svar!='nei':
        return 0
    return 1

def ITGK_skjekk(svar):
    global ITGK
    if svar=='ja':
        ITGK+=1
    elif svar!='nei':
        return 0
    return 1

def lekser_skjekk(svar):
    global lekser
    try:
        lekser.append(float(svar))
    except:
        return 0
    return 1

def snitt(n):
    try:
        return sum(lekser)/len(lekser)
    except ZeroDivisionError:
        return 0

def resultat():
    print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('Resultat av undersøkelse!')
    print(f' Antall kvinner: {kvinner}')
    print(f' Antall menn: {menn}')
    print(f' Antall personer som tar fag: {fag}')
    print(f' Antall personer som tar ITGK: {ITGK}')
    print(f' Antall timer i snitt brukt på lekser : {snitt(lekser)}')

skjekkliste=[kjønn_skjekk, alder_skjekk, fag_skjekk, ITGK_skjekk, lekser_skjekk]
spørsmålsliste=['Hvilket kjønn er du? [m/f]: ', 'Hvor gammel er du?: ', 'Tar du et eller flere fag? [ja/nei ]: ', 'Tar du '+virkelig+'ITGK?: ', 'Hvor mange timer bruker du daglig (i snitt) på lekser?: ']

def undersøkelse():
    global fag
    global alder
    global spørsmålsliste
    try:
        while True:
            alder=0
            print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            print('Velkommen til spørreundersøkelsen!\n')
            for x in range(len(spørsmålsliste)):
                spørsmålsliste[3]='Tar du '+virkelig+'ITGK?: '
                fag_gammel=fag
                ans=ny_input(spørsmålsliste[x])
                while not skjekkliste[x](ans):
                    ans=ny_input(spørsmålsliste[x])
                if x==2 and fag_gammel==fag:
                    break
                if alder:
                    break
    except:
        resultat()

undersøkelse()


# **a)** Be brukeren skrive inn kjønn og alder. Med for eksempel ***f*** for kvinne og ***m*** for mann, lagre disse i variablene **kjonn** og **alder**.
# 
# 
# 
# **b)** Sjekk om brukeren er innenfor tiltenkt aldersgruppe. Dersom brukeren er utenfor aldersgruppen, skriv en melding om at vedkommende ikke kan ta spørreundersøkelsen, og hopp tilbake til første spørsmål (kjønn).
# 
# 
# 
# **c)** Dersom brukeren er innenfor tiltenkt aldersgruppe, spør om brukeren tar et **fag**, med svaralternativene ja og nei. Deretter lagres svaret som en variabel fag. Ta utgangspunkt i denne variabelen når du avgjør om brukeren trenger å svare på de neste to spørsmålene eller ikke. Om noe annet svares, skal spørsmålet gjentas til et gyldig svaralternativ er gitt. 
# 
# 
# 
# **d)** Du skal nå spørre om brukeren tar ITGK og lagre svaret som en variabel **medlem_ITGK**, men spørsmålsteksten skal variere ut ifra alderen på brukeren
# 
# * Dersom brukeren er under 22 år skal spørsmålsteksten være: Tar du ITGK?
# * Ellers skal spørsmålsteksten være: Tar virkelig du ITGK?
# 
# 
# **e)** Spør brukeren hvor mange timer han/hun bruker i snitt daglig på lekser og lagre svaret i variabelen **timer_lekser**
# 
# 
# 
# **f)** Endre programmet ditt slik at de globale tellerne nevnt tidligere i oppgaven blir inkrementert i deloppgavene a til e.
# 
# 
# 
# **g)** Kjør programmet ditt, utfør noen undersøkelser, og avslutt ved å skrive hade. Sjekk at statistikken (verdiene av de globale tellerne) som skrives ut på slutten er korrekt.
# 
# **Eksempel på kjøring:**
# 
# ```
# Velkommen til spørreundersøkelsen!
#  
#  Hvilket kjønn er du? [f/m]: f
#  Hvor gammel er du?: 21
#  Tar du et eller flere fag? [ja/nei ]: bleh
#  Tar du et eller flere fag? [ja/nei ]: ja
#  Tar du ITGK? [ja/nei]: ja
#  Hvor mange timer bruker du daglig (i snitt) på lekser?: 2
#  
# Velkommen til spørreundersøkelsen!
#  
#  Hvilket kjønn er du? [f/m]: m
#  Hvor gammel er du?: 28
# Du kan dessverre ikke ta denne undersøkelsen
#  
# Velkommen til spørreundersøkelsen!
#  
#  Hvilket kjønn er du? [f/m]: m
#  Hvor gammel er du?: 25
#  Tar du et eller flere fag? [ja/nei ]: ja
#  Tar du virkelig ITGK?: nei
#  Hvor mange timer bruker du daglig (i snitt) på lekser?: 3
#  
# Velkommen til spørreundersøkelsen!
#  
#  Hvilket kjønn er du? [f/m]: f
#  Hvor gammel er du?: 18
#  Tar du et eller flere fag? [ja/nei ]: nei
#  
# Velkommen til spørreundersøkelsen!
#  
#  Hvilket kjønn er du? [f/m]: m
#  Hvor gammel er du?: 24
#  Tar du et eller flere fag? [ja/nei ]: hade
#  
# Resultat av undersøkelse!
#  Antall kvinner: 2
#  Antall menn: 2
#  Antall personer som tar fag: 2
#  Antall personer som tar ITGK: 1
#  Antall timer i snitt brukt på lekser : 2.5
#  ```
#  
# **h)** Vil det være mulig å hente ut svarene fra spørreundersøkelsen etter at vi har avsluttet programmet? Hvor er de i så fall lagret? Eventuelt hvorfor ikke?

# Ja, de vil være lagret i de globale variablene. Om du skal kjøre undersøkelsen på nytt, derimot, vil du ikke få lagt til den nye dataen med den forrige, siden den gamle slettes slettes. Det kan løses ved å lage while-løkken inni en funksjon den også.
