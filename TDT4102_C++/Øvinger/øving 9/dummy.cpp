#include "dummy.h"
#include <iostream>
#include <utility>
using namespace std;

void dummyTest() {
    Dummy a;
    *a.num = 4;
    Dummy b{a};//tror ikke dette går? 
    //det finnes ingen konstruktør for dummy med dummy
    Dummy c;
    c = a; //vi har vel ikke overlastet operatoren enda?
    cout << "a: " << *a.num << endl; //4
    cout << "b: " << *b.num << endl; //0? siden det er default
    cout << "c: " << *c.num << endl; //4. tror den skjønner litt av greia med =
    *b.num = 3;
    *c.num = 5;
    cout << "a: " << *a.num << endl;//4
    cout << "b: " << *b.num << endl;//3
    cout << "c: " << *c.num << endl;//5

    //jeg tok feil på det meste. sånn går det når det er snakk om pointere..
    //alle peker til samme sted i minnet, så øverst peker alle til 4 
    //så endres det til slutt til 5 i linje 16.

    cin.get(); // For å hindre at
    // programmet avslutter med en gang

    //tror det krasjer fordi det er ikke noe i cin-strømmen?
}

Dummy::Dummy(const Dummy& rhs){
    this->num = new int{*rhs.num};
}

Dummy& Dummy::operator=(Dummy rhs){
    std::swap(num, rhs.num);
    return *this;
}