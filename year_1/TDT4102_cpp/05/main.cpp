#include "std_lib_facilities.h"
#include "card.h"
#include "carddeck.h"
#include "blackjack.h"
#include <cstdlib>
#include <ctime>

/*
Oppgave 1 e)

Siden vi bruker enum blir koden mye mer lettleselig. Om vi som leser må ha et forhold til om suit[1] er kløver eller hjerter er mye å be om. 
Strenger hadde vært vanskeligere å oversette til noe som kan brukes i koden, men hadde væt like lette å lese som enum. 
*/

int main(){
	srand(static_cast<unsigned int>(time(nullptr)));
	int choice = -1;

	do{
		cout << "##################################\n";
		cout << "0	Exit\n";
		cout << "1	suitToString\n";
		cout << "2	rankToString\n";
		cout << "3	test Card\n";
		cout << "4	test CardDeck\n";
		cout << "5	test Player\n";
		cout << "6	playBlackjack\n";
		cout << endl;
		cout << "Enter a number ";
		cin >> choice;
		cout << endl;
		switch (choice){
			case 1:{
				cout << suitToString(Suit::clubs) << endl;
				break;
			}
			case 2:{
				cout << rankToString(Rank::king) << endl;
				break;
			}
			case 3:{
				Card KoH(Suit::hearts, Rank::king);
				cout << KoH.toString() << endl;
				cout << KoH.toStringShort() << endl;
				break;
			}
			case 4:{
				CardDeck deck;
				deck.print();
				deck.shuffle();
				deck.print();
				break;
			}
			case 5:{
				CardDeck deck;
				deck.shuffle();
				deck.print();
				vector<Card> hand;
				hand.push_back(deck.drawCard());
				hand.push_back(deck.drawCard());
				Player player(hand);
				cout << player.getScore() << endl;
				break;
			}
			case 6:{
				playBlackjack();
				break;
			}
			default:
				break;
		}
	}
	while (choice != 0);

	return 0;
}
