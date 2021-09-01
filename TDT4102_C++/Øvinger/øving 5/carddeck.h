#pragma once
#include "std_lib_facilities.h"
#include "card.h"

class CardDeck{
    vector<Card> cards;
    
    void swap(int a, int b);

    public:
        CardDeck();
        void print();
        void printShort();
        void shuffle();
        Card drawCard(); //pop and return the last card
};