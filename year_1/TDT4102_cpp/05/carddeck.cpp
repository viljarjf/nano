#include "std_lib_facilities.h"
#include "card.h"
#include "carddeck.h"
#include <cstdlib>
#include <ctime>



CardDeck::CardDeck(){
    vector<Card> cardDeck;
    for(int suit = 0; suit<4; suit++){
        for(int rank=2; rank<15; rank++){
            cardDeck.push_back(Card(Suit(suit),Rank(rank)));
        }
    }
    cards=cardDeck;
}

void CardDeck::swap(int a, int b){
    Card temp = cards[a];
    cards[a] = cards[b];
    cards[b] = temp;
}

void CardDeck::print(){
    for (Card c : cards){
        cout << c.toString() << endl;
    }
}

void CardDeck::printShort(){
    for (Card c : cards){
        cout << c.toStringShort() << endl;
    }
}

void CardDeck::shuffle(){
    for(int n = 0; n<cards.size(); n++){
        CardDeck::swap(n, rand()%cards.size()); //swap the n-th card with a random card, for every n
    }
}

Card CardDeck::drawCard(){
    Card c = cards.back();
    cards.pop_back();
    return c;
}
