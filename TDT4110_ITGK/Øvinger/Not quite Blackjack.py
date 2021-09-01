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
#     <li><a href="Sekantmetoden.ipynb">Sekantmetoden</a></li>
#     <li class="active"><a href="Not%20quite%20Blackjack.ipynb">Not quite Blackjack</a></li>
#         <li><a href="Funksjoner%20og%20Jupyter%20widgets.ipynb">Funksjoner og Jupyter widgets</a></li>
#     </ul>
#   </div>
# </nav>
# 
# 
# # Not quite Blackjack
# 
# **Læringsmål:**
# - Funksjoner
# - Betingelser
# - Løkker
# 
# **Starting Out with Python:**
# - Kap. 3: Decision Structures and Boolean Logic 
# - Kap. 4.2: The while Loop
# - Kap. 5: Functions
# 
# I denne oppgaven skal du lage spillet Blackjack med en vri. Vanlige Blackjack reglene som skal implementeres er som følger:
# 
# - Et ess teller enten 1 eller 11
# - Alle bildekort (J, Q, K) har verdi 10
# - Du får alltid utdelt to kort til å begynne med
# - Hvis den samlede verdien på kortene er over 21 er du ute
# - Et ess med 10 eller et bildekort er en «ekte» blackjack
# - Du vinner på én av tre måter:
#   - Du får ekte blackjack uten at dealer gjør det samme,
#   - Du oppnår en høyere hånd enn dealer uten å overstige 21, eller
#   - Din hånd har verdi mindre enn 21, mens dealerens hånd overstiger 21
# 
# Det som er annerledes med vår Blackjack, er at dealer bare får to kort, og at spilleren ikke får velge verdien ess vil ha. Spillet vil automatisk ta den verdien som er nærmest 21, men som ikke overstiger 21, og så fort en verdi for ess er satt, vil ikke denne endres senere. Dvs. at om man først får 1 (ess) og 8, vil verdien bli satt til 11+8=19. Om man deretter velger å trekke enda et kort og får 4, vil verdien bli 19+4=23, og man vil tape. Det blir altså ikke tatt hensyn til at 1+8+4<21. Om man derimot først fikk 4 og 8, og deretter fikk 1 (ess), så ville verdien blitt 4+8+1=13. 
# 
# **Eksempel på kjøring:**
# ```
# Dealers cards are 9 and ?
# Your score is: 16
# Do you want another card? (J/N) J
# Your score is: 19
# Do you want another card? (J/N) N
# Dealers score is: 18
# You won!
#   
# Dealers cards are 10 and ?
# Your score is: 20
# Do you want another card? (J/N) N
# Dealers score is: 21
# You lost
#   
#   
# Dealers cards are 10 and ?
# Your score is: 15
# Do you want another card? (J/N) J
# You got: 25
# You lost
# ```
# 
# ***Skriv koden din i kodeblokken under***

# In[1]:


import random
cards={}
cards['A']=[1,11]
cards['2']=2
cards['3']=3
cards['4']=4
cards['5']=5
cards['6']=6
cards['7']=7
cards['8']=8
cards['9']=9
cards['10']=10
cards['J']=10
cards['Q']=10
cards['K']=10

def pick_random_card():
    return random.choice(list(cards.keys()))

def dealer():
    return [pick_random_card(), pick_random_card()]

def card_sum(card_list):
    total=0
    for card in card_list:
        if card=='A' and total<=10:
            total+=max(cards[card])
        elif card=='A' and total>10:
            total+=min(cards[card])
        else:
            total+= cards[card]
    return total

def play_game():
    dealer_cards=dealer()
    dealer_sum=card_sum(dealer_cards)
    print(f'Dealers cards are: {dealer_cards[0]} and ?')
    player_cards=dealer()
    print('You have:', str(player_cards).replace('[','').replace(']','').replace("'",''))
    print(f'Your score is {card_sum(player_cards)}')
    while card_sum(player_cards)<21:
        if 'y' in input('Do you want another card? [y/n]: '):
            player_cards.append(pick_random_card())
            print('You have:', str(player_cards).replace('[','').replace(']','').replace("'",''))
            print(f'Your score is {card_sum(player_cards)}')
        else:
            break
    player_sum=card_sum(player_cards)
    print(f"\nDealers' cards are {dealer_cards[0]} and {dealer_cards[1]}")
    print('''Dealers' score is''', dealer_sum)
    if player_sum<dealer_sum or player_sum>21:
        print('You lost')
    elif player_sum==21 and len(player_cards)==2:
        print('You won with a Blackjack!')
    elif player_sum>dealer_sum:
        print('You beat the dealer! You won!')

play_game()

