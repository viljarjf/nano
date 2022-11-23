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
#     <li><a href="Aarstider.ipynb">Årstider</a></li>
#         <li ><a href="Tekstbasert%20spill.ipynb">Tekstbasert spill</a></li>
#     <li><a href="Sjakkbrett.ipynb">Sjakkbrett</a></li>
#     <li><a href="Billettpriser%20og%20rabatter.ipynb">Billettpriser og rabatter</a></li>
#     <li class="active"><a href="Skatteetaten.ipynb">Skatteetaten</a></li>
#     <li><a href="Epletigging.ipynb">Datamaskinen som tigget epler</a></li>
#     <li><a href="Andregradsligning.ipynb">Andregradsligning</a></li>
#     </ul>
#   </div>
# </nav>
# 
# # Skatteetaten
# 
# **Læringsmål:**
# 
# * Betingelser
# 
# **Starting Out with Python:**
# 
# * Kap. 3.1- 3.2
# * Kap. 3.4
#  
# 
# I denne oppgaven skal du lage et program som tar inn opplysninger om utleie av eiendom fra en bruker. Programmet vil så beregne hvor stor andel av inntekten som er skattbar.  
# 
# Regler for skatt finnes på Skatteetaten sine hjemmesider, men er ikke nødvendig å sette seg inn i: 
# 
# http://www.skatteetaten.no/no/Person/Selvangivelse/tema-og-fradrag/Jobb-og-utdanning/delingsokonomi/utleie-av-bolig-og-fritidsbolig/
# 
#  
# 
# 

# ### a)

# Lag et program som ber brukeren om opplysninger og svarer om inntekten er skattepliktig eller skattefri. 
# 
# Regler som må implementeres:
# 
# * Hvis du bruker minst halvparten av boligen du eier til eget bruk, beregnet etter utleieverdi, er det skattefritt å leie ut resten.
# *  Leier du ut mer enn halvparten av egen bolig, men for under 20 000 kr i året er det også skattefritt.
# * Leier du ut hele eller mer enn halvparten av egen bolig for over 20 000 kr i året er samtlige leieinntekter for hele året skattepliktige. 
# 
# **Eksempel på kjøring av kode:**
#  
# ```python
# INFO  
# Dette programmet besvarer om din utleie av egen bolig er skattepliktig. 
# Først trenger vi å vite hvor stor del av boligen du har leid ut.
# Angi dette i prosent, 100 betyr hele boligen, 50 betyr halve,
# 20 en mindre del av boligen som f.eks. en hybel.
# ----------------------------------------------------------------------  
# DATAINNHENTING:  
# Oppgi hvor mye av boligen som ble utleid: 65  
# Skriv inn hva du har hatt i leieinntekt: 45000   
# ----------------------------------------------------------------------  
# SKATTEBEREGNING:  
# Inntekten er skattepliktig  
# Skattepliktig beløp er 45000
# ```
# 
# ***Skriv koden din her:***

# In[1]:


def oppgave_a():   
    print('INFO\n'
    'Dette programmet besvarer om din utleie av egen bolig er skattepliktig.\n'
    'Først trenger vi å vite hvor stor del av boligen du har leid ut.\n'
    'Angi dette i prosent, 100 betyr hele boligen, 50 betyr halve,\n'
    '20 en mindre del av boligen som f.eks. en hybel.\n'
    '----------------------------------------------------------------------\n'
    'DATAINNHENTING: ')
    p = float(input('Oppgi hvor mye av boligen som ble utleid: '))
    i = int(input('Skriv inn hva du har hatt i leieinntekt: '))
    print('----------------------------------------------------------------------\n'
    'SKATTEBEREGNING: ')
    if p>50:
        if i>=20000:
            plikt='skattepliktig'
        else: 
            plikt='ikke skattepliktig'
            i=0
    else: 
        plikt='ikke skattepliktig'
        i=0
    print('Inntekten er', plikt)
    print('Skattepliktig beløp er', i)
oppgave_a()


# ### b)

# For å leie ut *sekundærbolig* eller *fritidsbolig* gjelder det særskilte regler. Lag et tilsvarende program som dekker disse behovene. (Se samme nettside for mer informasjon om ønskelig.)
# 
# Regler som må implementeres:
# 
# * Sekundærbolig:
#  * Utleie av sekundærbolig beskattes fra første krone.
# * Fritidsbolig:
#  * Der du helt eller delvis bruker fritidsboligen til fritidsformål, og selv bruker eiendommen i rimelig omfang over tid, så vil utleieinntekter inntil kr 10 000 være skattefrie.
#  * Av det overskytende beløp regnes 85 prosent som skattepliktig inntekt.
#  * Dersom fritidsboligen anses som utleiehytte blir det beskatning fra første krone.
#  * Om du leier ut flere enn en fritidsbolig vil grensen på 10 000 gjelde per fritidsbolig.
#  
# **Eksempel på kjøring av kode:**
#  
# ```python
# INFO
# Dette programmet besvarer om din utleie en annen type bolig,
# her sekundær- eller fritidsbolig, er skattepliktig.
# Først trenger vi å vite om du leier ut en sekundær- eller en fritidsbolig.
# ---------------------------------------------------------------------
# DATAINNHENTING:
# Skriv inn type annen bolig (sekundærbolig/fritidsbolig) du har leid ut: Fritidsbolig
#     
# INFO
# Du har valgt fritidsbolig.
# Nå trenger vi først å vite om fritidsboligen(e) primært brukes til utleie eller fritid.
# Deretter trenger vi å vite hvor mange fritidsbolig(er) du leier ut.
# Til slutt trenger vi å vite hvor store utleieinntekter du har pr. fritidsbolig.
# 
# ---------------------------------------------------------------------
# DATAINNHENTING:
# Skriv inn formålet med fritidsboligen(e): Fritid
# Skriv inn antallet fritidsboliger du leier ut: 3
# Skriv inn utleieinntekten pr. fritidsbolig: 15000
#     
# ---------------------------------------------------------------------
# SKATTEBEREGNING:
# Inntekten er skattepliktig
# Overskytende beløp pr. fritidsbolig er 5000
# Skattepliktig inntekt pr. fritidsbolig er 4250
# Totalt skattepliktig beløp er 12750
# ```
# 
# ***Skriv koden din her:***

# In[2]:


def printlinje():
    print('\n---------------------------------------------------------------------\n')
def oppgave_b():
    print('INFO\n'
    'Dette programmet besvarer om din utleie en annen type bolig,\n'
    'her sekundær- eller fritidsbolig, er skattepliktig.\n'
    'Først trenger vi å vite om du leier ut en sekundær- eller en fritidsbolig.')
    printlinje()

    print('DATAINNHENTING:')
    if 'fri' in input('Skriv inn type annen bolig (sekundærbolig/fritidsbolig) du har leid ut: ').lower():
        printlinje()

        print('INFO\n'
        'Du har valgt fritidsbolig.\n'
        'Nå trenger vi først å vite om fritidsboligen(e) primært brukes til enten utleie eller fritid.\n'
        'Deretter trenger vi å vite hvor store utleieinntekter du har pr. fritidsbolig.')
        printlinje()

        print('DATAINNHENTING:')
        formål=input('Skriv inn formålet med fritidsboligen(e): ').lower()
        inntekt=[int(x) for x in input('Skriv inn utleieinntekten pr. fritidsbolig, separert med komma(,): ').split(',')]
        printlinje()

        print('SKATTEBEREGNING:')
        if 'fritid' in formål:
            if max(inntekt)>10000:
              print('Inntekten er skattepliktig')
              print('Totalt skattepliktig beløp er:', sum([x-10000 for x in inntekt if x>10000])*0.85)
            else:
              print('Inntekten er ikke skattepliktig')
        elif 'leie' in formål:
          print('Inntekten er skattepliktig')
          print('Totalt skattepliktig beløp er:', sum(inntekt))
    else:
        printlinje()
        print('INFO\n'
        'Du har valgt sekundærbolig\n'
        'Inntekten fra disse beskattes fra første krone\n'
        'For beregningens skyld trenger vi å vite inntektene på sekundærboligen(e)')
        printlinje()

        print('DATAINNHENTING:')  
        inntekt=[int(x) for x in input('Skriv inn utleieinntekten pr. sekundærbolig, separert med komma(,): ').split(',')]
        printlinje()
        print('Inntekten er skattepliktig')
        print('Totalt skattepliktig beløp er:', sum(inntekt)) 
oppgave_b()


# ### c)

# Sett sammen del (a) og (b) til et større program som først spør brukeren hva som er blitt leid ut (egen bolig / sekundærbolig / fritidsbolig), og deretter regner ut passende skattesats. Du kan delvis kopiere koden fra de tidligere deloppgavene.
# 
# ***Skriv koden din her:***

# In[3]:


opg_c=input('Skriv inn "a" for privat/egen bolig, eller "b" for sekundær/fritidsbolig: ').lower()
if 'a' in opg_c:
    oppgave_a()
elif 'b' in opg_c:
    oppgave_b()

