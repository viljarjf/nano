#include "fibonacci.h"
#include "Matrix.h"
#include "dummy.h"
#include <iostream>
using namespace std;


int main(){
	int choice = -1;
	do{
		cout << "##################################\n";
		cout << "0	Exit\n";
		cout << "1	createFibonacci\n";
		cout << "2	test Matrix\n";
		cout << "3	dummyTest\n";
		cout << "Enter a number ";
		cin >> choice;
		cout << endl;
		switch (choice){
			case 1:{
				createFibonacci();
				break;
			}
			case 2:{
				testMatrix();
				break;
			}
			case 3:{
				dummyTest();
				break;
			}
			default:
				break;
		}
	}
	while (choice != 0);

	return 0;
}
