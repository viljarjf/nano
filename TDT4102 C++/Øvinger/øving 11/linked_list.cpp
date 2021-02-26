#include "linked_list.h"
#include "utdelt.h"

ostream& operator<<(ostream& os, Person& p){
    os << p.getFirstName();
    os << " ";
    os << p.getLastName();
    return os;
}

void insertOrdered(list<Person> &l, const Person& p){
    list<Person>::iterator itr;
    for (itr = l.begin(); itr != l.end(); itr++){
        if (itr->getFullName() > p.getFullName()){
            l.insert(itr, p);
            return;
        }
    }
    l.push_back(p);
}