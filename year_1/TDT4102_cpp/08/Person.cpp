#include "std_lib_facilities.h"
#include "Person.h"

Person::Person(string n, string em, Car* c) : name{n}, email{em}, car{c} {}

void Person::setName(string n){
    name=n;
}

string Person::getName() const{
    return name;
}

void Person::setEmail(string em){
    email=em;
}

string Person::getEmail() const{
    return email;
}

bool Person::hasAvailableSeats() const{
    if (car != nullptr){
        return car->hasFreeSeats();
    }
    return false;
}

ostream& operator<<(ostream& os, const Person p){
    os << "Name: " << p.name << endl;
    os << "Email: " << p.email << endl;
    os << "Available seats : " << (p.hasAvailableSeats() ? "yes" : "no") << endl;
    return os;
}
