#include <iostream>
#include "iterators.h"
#include "linked_list.h"
//#include "utdelt.h"

using namespace std;

vector<string> strVec {"first", "SECOND", "7h1rd"};

set<string> strSet {"first", "SECOND", "7h1rd"};

int main(){
	int choice = -1;
	do{
		cout << "##################################\n";
		cout << "0	Exit\n" << endl;
		cout << "1	printVector\n";
		cout << "2	printReverseVector\n";
		cout << "3	replace(vector)\n";
		cout << "4	printSet\n";
		cout << "5	printReverseSet\n";
		cout << "6	replace(set)\n";
		cout << "7	test linked lists\n";
		cout << "8 	testLinkedList\n";
		cout << "Enter a number ";
		cin >> choice;
		cout << endl;
		switch (choice){
			case 1:{
				printVector(strVec);
				break;
			}
			case 2:{
				printReverseVector(strVec);
				break;
			}
			case 3:{
				replace(strVec, "first", "først");
				printVector(strVec);
				break;
			}
			case 4:{
				printSet(strSet);
				break;
			}
			case 5:{
				printReverseSet(strSet);
				break;
			}
			case 6:{
				replace(strSet, "first", "først");
				printSet(strSet);
				break;
			}
			case 7:{
				list<Person> pl;
				pl.push_back(*new Person("Viljar", "Femoen"));
				insertOrdered(pl, *new const Person("Aruran", "Skrivesaker"));
				insertOrdered(pl, *new const Person("Richard", "Buckminster-Fuller"));
				insertOrdered(pl, *new const Person("Ivar", "Aasen"));
				insertOrdered(pl, *new const Person("Ivar", "Bbsen"));
				insertOrdered(pl, *new const Person("Xulu", "Zulu"));
				for (auto p : pl){
					cout << p << endl;
				}
				break;
			}
			case 8:{
				//testLinkedLists();
				break;
			}
			default:
				break;
		}
	}
	while (choice != 0);

	return 0;
}
