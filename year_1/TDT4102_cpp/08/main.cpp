#include "std_lib_facilities.h"
#include "Car.h"
#include "Person.h"
#include "Meeting.h"
#include "Graph.h"
#include "Window.h"
#include "MeetingWindow.h"


int main(){
	int choice = -1;
	do{
		cout << "##################################\n";
		cout << "0	Exit\n";
		cout << "1	test Person\n";
		cout << "2	test Meeting\n";
		cout << "3	GUI\n";
		cout << "Enter a number ";
		cin >> choice;
		cout << endl;
		switch (choice){
			case 1:{
				Person karl("Karl", "k.arl@gmail.com");
				cout << karl;
				Person kari{"Kari", "kari@stud.ntnu.no", new Car(3)};
				cout << kari;
				//i and l is really similar
				break;
			}
			case 2:{
				Meeting test{10, 12, 14, Campus::Trondheim, "Testmøte for å teste møte", new Person("Viljar", "viljar@mail.com", new Car(3))};
				test.addParticipants(new Person("Ivar", "mail@gmail.com"));
				test.addParticipants(new Person("Gunnhild", "G@m.no", new Car(8)));
				cout << test;
				break;
			}
			case 3:{
				MeetingWindow mwin{Point{100, 100}, 500, 400, "test"};
				gui_main();
				break;
			}
			default:
				break;
		}
	}
	while (choice != 0);

	return 0;
}
