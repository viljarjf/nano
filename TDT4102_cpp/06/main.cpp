#include "std_lib_facilities.h"
#include "oppgave_1.h"
#include "oppgave_2.h"
#include "oppgave_3.h"
#include "oppgave_4_5.h"
#include <ctime>


int main(){
	int choice = -1;
	do{
		cout << "##################################\n";
		cout << "0	Exit\n";
		cout << "1	writeToFile\n";
		cout << "2	createFileCopyWithLineNumbers\n";
		cout << "3	countLettersOfFile\n";
		cout << "4	test CourseCatalog\n";
		cout << "5	drawTempGraph\n";
		cout << "Enter a number ";
		cin >> choice;
		cout << endl;
		switch (choice){
			case 1:{
				writeToFile();
				break;
			}
			case 2:{
				createFileCopyWithLineNumber();
				break;
			}
			case 3:{
				countLettersOfFile();
				break;
			}
			case 4:{
				CourseCatalog cc;
				cc.addCourse("TMT4102", "Prosedyre- og objektorientert programmering");
				cout << cc << "\n\n";
				cc.addCourse("TMA4100", "Mattematikk 1");
				cc.addCourse("TMT4105", "Mattematikk 2");
				cout << cc << "\n\n";
				cc.addCourse("TMT4102", "C++");
				cout << cc << "\n\n";
				//cc.removeCourse("TMT4102");
				//cout << cc << "\n\n";
				cout << cc.getCourse("TMA4100") << endl;
				cc.saveToFile("testcc");
				CourseCatalog newcc;
				newcc.readFromFile("testcc");
				cout << newcc << "\n\n";
				break;
			}
			case 5:{
				drawTempGraph();
				break;
			}
			default:
				break;
		}
	}
	while (choice != 0);

	return 0;
}
