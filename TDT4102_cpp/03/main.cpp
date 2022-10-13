#include "cannonball.h"
#include "utilities.h"

#include "std_lib_facilities.h"
#include <cstdlib>
#include <ctime>
#include "Graph.h"
#include "Simple_window.h"


void testDeviation(double compareOperand, double toOperand, double maxError, string name);

void playTargetPractice();

void drawBallPath();

constexpr double maxError = 0.001;


int main(){
	srand(static_cast<unsigned int>(time(nullptr)));

	drawBallPath();
	
	//playTargetPractice();

	/*
	for (int y=0; y<35; y++){
		cout << randomWithLimits(0,9) << "  ";
	}
	*/

	//testCannonball();
	//testDeviation(posX(0, 50, 5), 250, maxError, "posX(0.0,50.0,5.0)");
	//keep_window_open();
	return 0;
}



void testDeviation(double compareOperand, double compareTo, double maxError, string name){
	cout << name << " == " << compareTo << ":\n";
	if (abs(compareOperand-compareTo)<=maxError){
		cout << "> true" << endl;
		return;
	}
	cout << "> false" << endl;
	return;
}


void playTargetPractice(){
	cout << "Target practice!" << endl;
	cout << "Your goal is to hit the target within 10 attempts. Good luck!" << endl;

	int target_pos = randomWithLimits(100, 1000);
	bool win = false;

	for (int attempt=0; attempt<10; attempt++){
		double theta = getUserInputTheta();
		double absVelocity = getUserInputAbsVelocity();
		vector<double> velocity = getVelocityVector(theta, absVelocity);
		double distanceToTarget = targetPractice(target_pos, velocity[0], velocity[1]);
		double time_in_air = flightTime(velocity[1]);
		
		if (abs(distanceToTarget)<=5){
			cout << "You hit the target! Congratulations!" << endl;
			cout << "You were " << abs(distanceToTarget) << " metres from the bullseye" << endl;
			win = true;
		}
		else{
			cout << "You missed by " << abs(distanceToTarget) << " metres." << endl;
			if (distanceToTarget>0){
				cout << "You need to shoot further." << endl;
			}
			else{
				cout << "You shot too far." << endl;
			}
		}
		cout << "The ball spent ";
		printTime(time_in_air);
		cout << " in the air" << endl;
		cout << "\n\n";

		if (win){
			break;
		}
	}
	if (!win){
		cout << "You didn't hit the target." << endl;
	}
	return;
}

using namespace Graph_lib;

void drawBallPath(){
	cout << "Target practice!" << endl;
	cout << "Your goal is to hit the target within 10 attempts. Good luck!" << endl;
	cout << "Click the \"Next\"-button to proceed" << endl;

	int target_pos = randomWithLimits(100, 1000);
	bool win = false;

	Simple_window window{Point{600, 100}, 1000, 500, "Ball path"};
	int segments = 100;
	Point origo = Point{10, 490};
	vector<Open_polyline> paths(10);

	Polygon target;
	target.add(Point{origo.x+target_pos-5, origo.y});
	target.add(Point{origo.x+target_pos+5, origo.y});
	target.add(Point{origo.x+target_pos+5, origo.y+3});
	target.add(Point{origo.x+target_pos-5, origo.y+3});
	target.set_color(Color::green);
	target.set_fill_color(Color::green);
	window.attach(target);

	Open_polyline bakken;
	bakken.add(origo);
	bakken.add(Point{1000, origo.y});
	bakken.set_color(Color::black);
	window.attach(bakken);

	window.wait_for_button();

	for (int attempt=0; attempt<10; attempt++){
		double theta = getUserInputTheta();
		double absVelocity = getUserInputAbsVelocity();
		vector<double> velocity = getVelocityVector(theta, absVelocity);
		double distanceToTarget = targetPractice(target_pos, velocity[0], velocity[1]);
		double time_in_air = flightTime(velocity[1]);

		for (double t=0; t<=time_in_air; t+=time_in_air/segments){
			paths[attempt].add(Point{origo.x+static_cast<int>(posX(0, velocity[0], t)), origo.y-static_cast<int>(posY(0, velocity[1], t))});
		}
		paths[attempt].set_color(Color::red);

		window.attach(paths[attempt]);

		if (abs(distanceToTarget)<=5){
			cout << "You hit the target! Congratulations!" << endl;
			cout << "You were " << abs(distanceToTarget) << " metres from the bullseye" << endl;
			win = true;
		}
		else{
			cout << "You missed by " << abs(distanceToTarget) << " metres." << endl;
		}
		cout << "The ball spent ";
		printTime(time_in_air);
		cout << " in the air" << endl;
		cout << "\n\n";		

		window.wait_for_button();

		if (win){
			break;
		}
	}
	if (!win){
		cout << "You didn't hit the target." << endl;
	}
	return;
}