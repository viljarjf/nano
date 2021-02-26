#include <iostream>
#include <string>

#include "readInput.h"
#include "graphWindow.h"

using namespace std;
using namespace Graph_lib;

int main(){
	int choice = -1;
	do{
		cout << "##################################\n";
        cout << "Please choose wether to choose a file to read from, or input numbers yourself\n\n";
		cout << "0	Exit" << endl;
        cout << "1  read from file\n";
        cout << "2  enter manually\n\n";
		cout << "Enter a number ";
		cin >> choice;
		cout << endl;

        vector<int> ints;
		switch (choice){
			case 1:{
                cout << "Please enter filename (with extension, eg. filename.txt): ";
                string filename;
                cin >> filename;
				vector<int> ints = readFromFile(filename);
				break;
			}
            case 2:{
                cout << "Please enter your numbers, separated by commas: ";
                vector<int> ints = manualInput();
                break;
            }
			default:
				break;
		}
        //additional early check for exiting
        if (choice == 0){
            break;
        }
        //convert the input of ints to points
        vector<Point> points = intToPoints(ints);
        //initialize the window
        GraphWindow(points, Point{100, 100}, 600, 600);
        return gui_main();
	}
	while (choice != 0);

	return 0;
}
