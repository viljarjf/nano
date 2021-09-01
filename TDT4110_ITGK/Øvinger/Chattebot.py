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
#     <li ><a href="Tannfeen.ipynb">Tannfeen</a></li>
#         <li class="active"><a href="Chattebot.ipynb">Chattebot</a></li>
#     <li ><a href="Matriseaddisjon.ipynb">Matriseaddisjon</a></li>
#     <li ><a href="Intro%20til%20numpy-arrays.ipynb">Intro til numpy-arrays</a></li>
#     </ul>
#   </div>
# </nav>
# 
# # Chattebot
# 
# **Læringsmål:**
# 
# * Lister
# 
# **Starting Out with Python:**
# 
# * Kap. 7.1-7.3
# 
# **I denne oppgaven skal du skrive et større program. For denne typen oppgaver kan det være mer praktisk å laste ned python og eventuelt en IDE (Et område man programmerer i på sin egen maskin). Ta derfor en kikk [her](https://docs.google.com/document/d/17tS0maWyzORUsIjmCVEszfqrl2X4By-Cy2Sw3ENG5lA/edit?usp=sharing) før du begynner. Det er fortsatt mulig å gjøre oppgaven i Jupyter dersom du ikke ønsker å jobbe lokalt, selv om det ikke er anbefalt.**
# 
# I denne oppgaven skal du lage et program som simulerer en datavenn du kan snakke med, en såkalt "chatbot".
# 
# **Oppgave:** Skriv koden som mangler for å fullføre programmet.
# 
# Hovedfunksjonen til programmet er følgende:
# 
# Spørre brukeren om navnet.
# Stille et tilfeldig spørsmål fra en liste av spørsmål til brukeren der navnet inngår.
# La brukeren få svare.
# Stille et tilfeldig oppfølgingsspørsmål, der svaret fra brukeren er med.
# Gi en tilfeldig kommentar til brukeren.
# Programmet skal avsluttes ved at brukeren gir svaret “hade”. Kildekoden er godt dokumentert med kommentarer og alle steder som mangler kode er markert med “MANGLER KODE HER!!!”. Kildekoden er gitt under, så start med å kopiere og lime denne inn i en python fil, eventuelt jobb direkte i kodeboksen.
# 
# Husk: **pass** i starten av while-løkken må fjernes når dere begynner å skrive koden deres. 

# In[2]:


# vim:set fileencoding=latin-1:
import random  # Importerer modulen random (generere tilfeldige tall)


# Funksjon:     pick_sentence
# Beskrivelse:  Plukker ut en tilfeldig tekststreng fra en liste av tekstsetninger
# Input:        En liste av tekststrenger
# Ouput:        En tekststreng
def pick_sentence(sentences):
    return sentences[random.randint(0, len(sentences) - 1)]


# Funksjon:     print_sentence
# Beskrivelse:  Skriver ut tre tekststrenger på ei linje til konsoll.
#               Det skal være mellomrom (space) mellom tekststreng en og to.
#               Det skal ikke være mellomrom (space) mellom tekststreng to og tre.
# Input:        Tre tekststrenger
# Output:       Ingen
def print_sentence(sentence_1, sentence_2, sentence_3):
    print(sentence_1, sentence_2+sentence_3)

# Funksjon:     intro_text
# Beskrivelse:  Skriver en velkomsttekst til konsoll som skal inneholde:
#               20 linjeskift
#               Setningen: "Hei, jeg heter HAL og vil gjerne snakke med deg."
#               Setningen: "Ikke start svar med stor bokstav og bruk hele setninger."
#               Setningen: "Skriv 'hade' hvis du vil avslutte samtalen"
#               Setningen: "**************************************************"
#               1 linjeskift
# Input:        Ingen
# Output:       Ingen
def intro_tekst():
    print('\n'*20)
    print("Hei, jeg heter HAL og vil gjerne snakke med deg.")
    print("Ikke start svar med stor bokstav og bruk hele setninger.")
    print("(Navnet ditt kan du skrive med stor bokstav :) )")
    print("Skriv 'hade' hvis du vil avslutte samtalen")
    print("**************************************************\n")

# Funksjon:     main
# Beskrivelse:  Hovedfunksjonen i programmet
# Input:        Ingen
# Output:       Ingen
def main():
    # Initialisering av variabler
    answer = "ikke hade"  # Sørger for at while-løkka kjører første gang

    # En liste av spørsmål
    questions = ['Hva gjør du', 'Hvordan går det', 'Hvorfor heter du',
                 'Liker du å hete', 'Føler du deg bra', 'Hva har du gjort idag',
                 'Hva tenker du om framtida', 'Hva gjør deg glad', 'Hva gjør deg trist']

    # En liste av oppfølgningsspørsmål
    follow_ups = ['Hvorfor sier du', 'Hva mener du med', 'Hvor lenge har du sagt',
                  'Hvilke tanker har du om', 'Kan du si litt mer om',
                  'Når tenkte du første gang på']

    # En liste av responser
    responses = ['Fint du sier det', 'Det skjønner jeg godt', 'Så dumt da', 'Føler meg også sånn',
                 'Blir trist av det du sier', 'Så bra', 'Du er jammen frekk']

    # Skriv velkomsttekst til konsoll vha. funksjonen intro_text
    intro_tekst()

    # Spør brukeren om navnet og lagre svaret i en variabel
    navn = input('Hva er navnet ditt? ')

    # Programmet kjører i løkke helt til brukeren svarer "hade"
    while answer != "hade":
        pass

        # NB: All kode her må skrives med to innrykk!!!

        # Plukk ut et tilfeldig spørsmål fra lista questions
        # ved hjelp av funksjonen pick_sentence
        spm=pick_sentence(questions)

        # Skriv spørsmålet etterfulgt av navnet til brukeren
        # og et spørsmålstegn ved hjelp av funksjonen print_sentence
        print_sentence(spm, navn, '?')

        # Spør brukeren om et svar med teksten "Svar: " og lagre
        # resultatet i en variabel
        answer = input('Svar: ')
        if answer=='hade':
            break

        # Plukk ut et tilfeldig oppfølgingsspørsmål fra lista follow_ups
        # ved hjelp av funksjonen pick_sentence
        opf = pick_sentence(follow_ups)

        # Skriv oppfølgningsspørsmålet sammen med svaret fra brukeren
        # og et spørsmålstegn ved hjelp av funksjonen print_sentence
        print_sentence(opf, answer, '?')

        # Spør brukeren om et svar med teksten "Svar: " uten å lagre
        # resultatet til variabel
        answer = input('Svar: ')

        # Plukk ut en tilfeldig respons fra lista responses
        # ved hjelp av funksjonen pick_sentence
        res = pick_sentence(responses)

        # Skriv reponsen sammen med navnet til brukeren
        # og et punktum (".") ved hjelp av funksjonen print_sentence
        print_sentence(res, navn, '.')


main()


# **Eksempel på kjøring:**
# 
# ```
# Hei , Jeg heter HAL og vil gjerne snakke med deg!
#  Ikke start svar med stor bokstav og bruk hele setninger .
#  Skriv 'hade ' hvis du vil avslutte  
#  **************************************************
# Hva heter du? Bob Bernt
# Hvorfor heter du  Bob Bernt?
#  Svar : mamma liker det navnet
# Hvilke tanker har du om  mamma liker det navnet?
#  Svar : litt ekkelt
# Så bra  Bob Bernt.
# Hva gjør deg trist  Bob Bernt?
#  Svar : ikke noe mer sjokolade
# Hvorfor sier du  ikke noe mer sjokolade?
#  Svar : hæ?
# Så dumt da  Bob Bernt.
#  Hva tenker du om framtida  Bob Bernt?
#  Svar : hade
# Hva mener du med hade?
#  Svar : ku
# Blir trist av det du sier  Bob Bernt.
# ```
