#include <forward_list>
#include <iostream>
#include <list>
#include <string>

using namespace std;

class Person{
private:
    string firstName;
    string lastName;
public:
    Person(const string& f, const string& l) : firstName(f), lastName(l){}
    string getFirstName() const {return firstName;}
    string getLastName() const {return lastName;}

    bool operator <(const Person& p) const;
    friend ostream& operator <<(ostream& out, const Person& p);
};

bool Person::operator <(const Person& p) const{
    //concatenate last + first and compare
    return (lastName + firstName) < (p.lastName + p.firstName);
}

ostream& operator <<(ostream& out, const Person& p){
    out << p.lastName << ", " << p.firstName;
    return out;
}

void insertOrdered(list<Person> &p, const Person& person){
  // pit has type list<Person>::iterator
	for (auto pit = p.begin(); pit != p.end(); ++pit){	//Iterate through the list
		if (person  < *pit){			//until we reach an element that is larger than the element we wish to insert
			p.insert(pit, person);		//and insert out element at the found position.
			return;
		}
	}
	p.push_back(person);				//If there is no element in the list larger than the one we wish to insert,
}							//the element is inserted at the back of the list.

void testStdLists(){
    cout << "list:" << '\n';

    list<Person> persons2;
    insertOrdered(persons2, Person("Trond", "Aalberg"));
    insertOrdered(persons2, Person("Trine", "Bakke"));
    insertOrdered(persons2, Person("Arne", "Aalberg"));
    insertOrdered(persons2, Person("Ola", "Norman"));
    insertOrdered(persons2, Person("Kari", "Norman"));

    // we could have used iterators to print, but we prefer range-based for-loops
    for (const auto& p : persons2){
        cout << p << '\n';
    }
}

