#include "cannonball.h"
#include "std_lib_facilities.h"

double acclY(){
    return -9.81;
}

double velY(double initVelocityY, double time){
    return initVelocityY + acclY()*time;
}

double posX(double initPosition, double initVelocity, double time){
    return initPosition + initVelocity*time;
}

double posY(double initPosition, double initVelocity, double time){
    return initPosition + initVelocity*time + 0.5*acclY()*time*time;
}

void printTime(double time){
    int hours =0;
    int minutes = 0;
    if (time>=3600){
        hours= static_cast<int>(time)/3600;
        time -= 3600*hours;
    }
    if (time>=60){
        minutes = static_cast<int>(time)/60;
        time -= 60*minutes;
    }
    cout << hours << " hours, " << minutes << " minutes, and " << time << " seconds";
}

double flightTime(double initVelocityY){
    return -2*initVelocityY/acclY();
}

double getUserInputTheta(){
    double theta = -1;
    cout << "Please enter an angle: ";
    cin >> theta;
    return theta;
}

double getUserInputAbsVelocity(){
    double v = -1;
    cout << "Please enter a velocity: ";
    cin >> v;
    return v;
}

double degToRad(double deg){
    constexpr double pi = 3.14159265;
    return deg/180.0*pi;
}

double getVelocityX(double theta, double absVelocity){
    return absVelocity*cos(degToRad(theta));
}
double getVelocityY(double theta, double absVelocity){
    return absVelocity*sin(degToRad(theta));
}

vector<double> getVelocityVector(double theta, double absVelocity){
    vector<double> v;
    v.push_back(getVelocityX(theta, absVelocity));
    v.push_back(getVelocityY(theta, absVelocity));
    return v;
}

double getDistanceTraveled(double velocityX, double velocityY){
    double time = flightTime(velocityY);
    return posX(0, velocityX, time);
}

double targetPractice(double distanceToTarget, double velocityX, double velocityY){
    return distanceToTarget - getDistanceTraveled(velocityX, velocityY);
}


void testCannonball(){
	cout << setw(7) << "T=0" << setw(7) << "T=2.5" << setw(7) << "T=5" << endl;
	//acclX
	for (double x=0; x<=5; x+=2.5){
		cout << setw(7) << 0;
	}
	cout << " acclX" << endl;

	//acclY
	for (double x=0; x<=5; x+=2.5){
		cout << setw(7) << acclY();
	}
	cout << " acclY" << endl;

	//velX
	for (double x=0; x<=5; x+=2.5){
		cout << setw(7) << 50.0;
	}
	cout << " velX" << endl;

	//velY
	for (double x=0; x<=5; x+=2.5){
		cout << setw(7) << velY(25, x);
	}
	cout << " velY" << endl;

	//posX
	for (double x=0; x<=5; x+=2.5){
		cout << setw(7) << posX(0, 50, x);
	}
	cout << " posX" << endl;

	//posY
	for (double x=0; x<=5; x+=2.5){
		cout << setw(7) << posY(0, 25, x);
	}
	cout << " posY" << endl;
}