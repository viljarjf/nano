#include "std_lib_facilities.h"
#include "card.h"
#include "carddeck.h"
#include "blackjack.h"

Player::Player(vector<Card> h) : hand{h}, score{0} {}

Player::Player(){//apparently c++ needs a constructor without parameters to work...
    vector<Card> h;
    hand = h;
    score = 0;
}

void Player::drawCard(CardDeck &deck){
    hand.push_back(deck.drawCard());
}

int Player::getScore(){
    score = 0;
    int aces =0;
    for (Card c : hand){
        if (static_cast<int>(c.getRank())<=10){//2 to 10
            score += static_cast<int>(c.getRank());
        }
        else if (static_cast<int>(c.getRank())<14){ //J to K
            score += 10;
        }
        else{ //A, additional logic for 1 vs 11 points below
            aces++;
            score += 11;
        }
        if (score>21 && aces>0){ //aces can be 11 or 1. If you overflow but have an ace counted as 11, recount as 1. Do this for every ace necessary. 
                score -= 10;
                aces--;
        }
    }
    return score;
}

void Player::printHand(){
    for(Card c : hand){
        cout << " -  " << c.toString() << endl;
    }
}

void Player::printLastCard(){
    cout << " -  " << hand[hand.size()-1].toString() << endl; //find the last card drawn, convert it tp a string, and print it.
}

bool Player::isBlackjack(){
    if (hand.size()==2 && score==21){
        return true;
    }
    return false;
}

Blackjack::Blackjack(){
    vector<Player> playerList;
    CardDeck d;
    d.shuffle();
    vector<Card> playerHand;
    vector<Card> dealerHand;
    for(int x=0; x<2; x++){
        playerHand.push_back(d.drawCard());
        dealerHand.push_back(d.drawCard());
    }
    Player pl(playerHand);
    Player de(dealerHand);
    playerList.push_back(pl);

    players = playerList;
    dealer = de;
    deck = d;
};

Blackjack::Blackjack(int playerAmount){
    vector<Player> playerList;
    CardDeck d;
    d.shuffle();

    vector<Card> dealerHand;    
    for(int x=0; x<2; x++){
        dealerHand.push_back(d.drawCard());
    }
    Player de(dealerHand);

    for(int n=0; n<playerAmount; n++){
        vector<Card> playerHand; 
        for(int x=0; x<2; x++){
            playerHand.push_back(d.drawCard());
        }
        Player pl(playerHand);
        playerList.push_back(pl);
    }

    players = playerList;
    dealer = de;
    deck = d;
};


void Blackjack::playPlayer(int playerNumber){
    Player &player = players[playerNumber]; //will throw an error if the player does not exist
    cout << "You have:\n";
    player.printHand();
    do{
        cout << "Do you want another card? (Y/N) ";
        char choice;
        cin >> choice;
        if (!cin){
            cout << "Please answer with Y or N (as yes or no). ";
            continue;
        }
        if (choice=='Y' || choice=='y'){
            player.drawCard(deck);
        }
        else if(choice=='N' || choice=='n'){
            break;
        }
        else{
            cout << "Please answer with Y or N (as yes or no). ";
            continue;
        }
        cout << "You drew: ";
        player.printLastCard();
        cout << "Your score is: " << player.getScore() << endl;
    }
    while(player.getScore() <= 21);
    cout << "You ended up with:" << endl;
    player.printHand();
};

void Blackjack::playDealer(){
    cout << "The dealer has:\n";
    dealer.printHand();
    while(dealer.getScore() < 17){
        dealer.drawCard(deck);
        cout << "The dealer drew ";
        dealer.printLastCard();
        cout << "Dealer's score is: " << dealer.getScore() << endl;
    }
    cout << "The dealer ended up with:" << endl;
    dealer.printHand();
}

bool Blackjack::winCheck(int playerNumber){
    int score=players[playerNumber].getScore();

    if (score > 21){ //lose if score>21
        return false;
    }
    else if(dealer.getScore() > 21){ //win if dealer has score>21
        return true;
    }
    else if (score > dealer.getScore()){ // win if you have better score than dealer
        return true;
    }
    else if (players[playerNumber].isBlackjack() && !dealer.isBlackjack()){ 
        //win if you have blackjack and the dealer does not. Also true if the dealer has 21pts and not blackjack.
        return true;
    }
    else{
        return false;
    }
}

void Blackjack::printDealerFirstCard(){
    dealer.printLastCard();
}

void Blackjack::printDeck(){
    deck.print();
}

void playBlackjack(){
    cout << "Please enter number of players: ";
    int numOfPlayers=-1;
    do{
        cin >> numOfPlayers;
        if (!cin || numOfPlayers<1){
            cout << "\nPlease enter a positive whole number ";
        }
    }
    while (numOfPlayers<0);

    Blackjack blackjack(numOfPlayers);
    cout << "The dealer has: ";
    blackjack.printDealerFirstCard();

    for(int x=0; x<numOfPlayers; x++){
        cout << "#################################################\n";
        cout << "Player " << x+1 << "'s turn" << endl;
        blackjack.playPlayer(x);
        cout << "\n\n";
    }

    cout << "#################################################\n";
    cout << "Dealer's turn" << endl;
    blackjack.playDealer();
    cout << "\n\n";

    for(int x=0; x<numOfPlayers; x++){
        string message = blackjack.winCheck(x) ? 
        " beat the dealer and won!" :
        " lost...";

        cout << "Player " << x+1 << message << endl;
    }
}


