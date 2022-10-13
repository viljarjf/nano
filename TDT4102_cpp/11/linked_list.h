#pragma once 
#include <string>
#include <iostream>
#include <list>

using namespace std;

class Person{
    string firstname;
    string lastname;

    public: 
    Person(string fn, string ln): firstname{fn}, lastname{ln} {}
    string getFullName() const {return firstname+lastname;}
    string getFirstName() {return firstname;}
    string getLastName() {return lastname;}
};

ostream& operator<<(ostream&, Person& p);

void insertOrdered(list<Person> &l, const Person& p);