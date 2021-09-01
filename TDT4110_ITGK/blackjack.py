# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 12:48:22 2019

@author: Bruker
"""

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

def win_check(player_cards, dealer_cards):
    player_sum = card_sum(player_cards)
    dealer_cards = card_sum(dealer_cards)
    if player_sum <= dealer_sum or player_sum > 21:
        return(0)
    elif player_sum == 21 and len(player_cards) == 2:
        return(1)
    elif player_sum > dealer_sum:
        return(2)

def dealer_play(player_cards, dealer_cards):
    if win_check(player_cards, dealer_cards) in [0,2]:
        return
    dealer_cards.append(pick_random_card())
    return dealer_cards

def play_game():
    dealer_cards=dealer()
    dealer_sum=card_sum(dealer_cards)
    print(f'Dealers cards are: {dealer_cards[0]} and ?')
    player_cards=dealer()
    print('You have:', str(player_cards).replace('[','').replace(']','').replace("'",''))
    print(f'Your score is {card_sum(player_cards)}')
    while card_sum(player_cards) <= 21:
        if 'y' in input('Do you want another card? [y/n]: '):
            player_cards.append(pick_random_card())
            print('You have:', str(player_cards).replace('[','').replace(']','').replace("'",''))
            print(f'Your score is {card_sum(player_cards)}')
        else:
            break

    print(f"\nDealers' cards are {dealer_cards[0]} and {dealer_cards[1]}")
    print('''Dealers' score is''', dealer_sum)

    win_list = ['You lost', 'You won with a Blackjack!', 'You beat the dealer! You won!']
#play_game()

def F(x):
    return 0.5*(x+2/x)

def newton(f,df, x0, feil):
    x=x0-f(x0)/df(x0)
    #print(x)
    #if abs(x0-x)>feil:
    #    return newton(f, df, x, feil)
    #return x
    if feil>=1:
        return newton(f, df, x, feil-1)
    return x

def g(x):
    return 4*x**3-14*x-2

def dg(x):
    return 12*x**2-14



