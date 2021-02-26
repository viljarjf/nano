#pragma once
#include "std_lib_facilities.h"

class Animal{
    protected:
        string name;
        int age;
    public:
        Animal(string n, int a);
        virtual string toString() =0;
};

class Cat: public Animal{
    public:
        Cat(string n, int a);
        string toString() override;
};

class Dog: public Animal{
    public:
        Dog(string n, int a);
        string toString() override;
};

void testAnimal();