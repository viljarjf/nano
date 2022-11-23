# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 09:46:16 2019

@author: Bruker
"""
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
