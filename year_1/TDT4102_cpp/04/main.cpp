#include "std_lib_facilities.h"
#include "utilities.h"
#include "masterMind.h"
#include "tests.h"
#include "masterVisual.h"
#include "Graph.h"
#include "Simple_window.h"


/* 
Oppgave 1 a)

Siden incrementByValueNumTimes er Pass-by-value vil
ikke v0 endres når den kalles opp. Hadde funksjonen heller vært 
Pass-by-refrence, ville v0 vært lik result når de ble printet.


Oppgave 1 e)

Denne funksjonen bør bruke referanser, ettersom det så vidt jeg vet 
ikke går an å returnere to tall i samme funksjon. Hvis ikke kunne man
gjort noe sånt som 
a, b = swapNumbers(a, b);
Med referanser holder det med
swapNumbers(a, b);

*/

int main(){
	using namespace Graph_lib;
	srand(static_cast<unsigned int>(time(nullptr)));

	int choice = 0;
	do{
		cout << "\n#######################################" << endl;
		cout << "0	Exit\n" << "1	testCallByValue\n"
			 << "2	testCallByRefrence\n" << "3	testVectorSorting\n"
			 << "4	test struct Student\n" << "5	testString\n" 
			 << "6	test readInputToString\n" << "7	playMasterMind\n" << endl;

		cout << "Choose a number: ";
		cin >> choice;
		cout << endl;

		switch(choice){
			case 1:{
				testCallByValue();
				break;
			}
			case 2:{
				testCallByRefrence();
				break;
			}
			case 3:{
				testVectorSorting();
				break;
			}
			case 4:{
				Student student;
				student.name = "Viljar";
				student.studyProgram = "Nanoteknologi";
				student.age = 1337;
				printStudent(student);
				break;
			}
			case 5:{
				testString();
				break;
			}
			case 6:{
				string test = readInputToString(6, 'A', 'p');
				cout << test << endl;
				break;
			}
			case 7:{
				playMasterMind();
				break;
			}
			default:
				break;
		}
	}
	while (choice != 0);

	return gui_main();
}