#include "std_lib_facilities.h"
#include "oppgave_1.h"
#include "Graph.h"

Animal::Animal(string n, int a) : name{n}, age{a} {}

string Animal::toString(){
    return "Animal: "+name+", "+to_string(age);
}



Cat::Cat(string n, int a) : Animal(n, a) {}

string Cat::toString(){
    return "Cat: "+name+", "+to_string(age);
}



Dog::Dog(string n, int a) : Animal(n, a) {}

string Dog::toString(){
    return "Dog: "+name+", "+to_string(age);
}

void testAnimal(){
    /*
    Animal a("dyr", 10); 
    cout << a.toString() << endl;// her får vi feil når vi gjør toString pure virtual
*/
    Cat c("katt", 100);
    cout << c.toString() << endl;

    Dog d("hund", 1000);
    cout << d.toString() << endl;

    using namespace Graph_lib;
    Vector_ref<Animal> animals;
    //animals.push_back(a); //her også, Animal er nå abstrakt så vi kan ikke ha en instans av klassen
    animals.push_back(c);
    animals.push_back(d);
    for(int x=0; x<animals.size(); x++){
        cout << animals[x].toString() << endl;
    }
}