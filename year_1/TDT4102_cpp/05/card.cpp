#include "card.h"
#include "std_lib_facilities.h"

string suitToString(Suit suit){
    map<Suit, string> suitMap{
        {Suit::clubs, "Clubs"},
        {Suit::diamonds, "Diamonds"},
        {Suit::hearts, "Hearts"},
        {Suit::spades, "Spades"}
    };
    return suitMap[suit];
}

string rankToString(Rank rank){
    map<Rank, string> rankMap{
        {Rank::two, "Two"},
        {Rank::three, "Three"},
        {Rank::four, "Four"},
        {Rank::five, "Five"},
        {Rank::six, "Six"},
        {Rank::seven, "Seven"},
        {Rank::eight, "Eight"},
        {Rank::nine, "Nine"},
        {Rank::ten, "Ten"},
        {Rank::jack, "Jack"},
        {Rank::queen, "Queen"},
        {Rank::king, "King"},
        {Rank::ace, "Ace"}
    };

    return rankMap[rank];
}

Card::Card(Suit suit, Rank rank) : s{suit}, r{rank} {}

Suit Card::getSuit(){
    return s;
} 

Rank Card::getRank(){
    return r;
}
string Card::toString(){
    return rankToString(getRank()) + " of " + suitToString(getSuit());
}
string Card::toStringShort(){ //Dette kunne vært gjort som over, på bare en linje, men det er litt mer leselig sånn her. 
    char suit = suitToString(getSuit())[0];
    int rank = static_cast<int>(getRank());
    string cardName = "";
    cardName += suit;
    cardName += to_string(rank);
    return cardName;
}

