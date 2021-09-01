#include "Car.h"

//alle disse er enkle one-liners, kunne fint vært i headerfilen imo

Car::Car(int fS) : freeSeats{fS} {}

bool Car::hasFreeSeats() const{
    return (freeSeats>0);
}

void Car::reserveFreeSeat(){
    freeSeats--;
}