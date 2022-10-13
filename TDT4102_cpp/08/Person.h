#pragma once
#include "std_lib_facilities.h"
#include "Car.h"

class Person{
    string name;
    string email;
    Car * car;

    public:
        Person(string n, string em, Car* c= nullptr);

        void setName(string n);
        string getName() const;

        void setEmail(string em);
        string getEmail() const;

        bool hasAvailableSeats() const;

        friend ostream& operator<<(ostream&, const Person);
};

