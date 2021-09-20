#pragma once
#include "std_lib_facilities.h"
#include "card.h"
#include "carddeck.h"

class Player{
    vector<Card> hand;
    int score;

    public:
        Player();
        Player(vector<Card> h);
        void drawCard(CardDeck &deck);
        void printHand();
        void printLastCard();
        int getScore();
        bool isBlackjack();
};

class Blackjack{
    vector<Player> players;
    Player dealer;
    CardDeck deck;

    public:
        Blackjack();
        Blackjack(int playerAmount);
        void playPlayer(int playerNumber);
        void playDealer();
        bool winCheck(int playerNumber);
        void printDealerFirstCard();
        void printDeck();
};

void playBlackjack();

//TODO dobling

