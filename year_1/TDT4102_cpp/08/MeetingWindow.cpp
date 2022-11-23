#include "std_lib_facilities.h"
#include "Meeting.h"
#include "Person.h"
#include "Graph.h"
#include "MeetingWindow.h"

MeetingWindow::MeetingWindow(Point xy, int w, int h, const string& title):
    Window{xy, w, h, title},
    quitBtn{quitBtnAnchor, btnW, btnH, "Quit", cb_quit},
    personName{personNameAnchor, fieldW, fieldH, "Name"},
    personEmail{personEmailAnchor, fieldW, fieldH, "Email"},
    personNewBtn{personNewBtnAnchor, btnW, btnH, "Add", cb_new_person},
    printPeopleBtn{printPeopleBtnAnchor, btnW, btnH, "Print", cb_printPeople}
    {
        attach(quitBtn);
        attach(personName);
        attach(personEmail);
        attach(personNewBtn);
        attach(printPeopleBtn);
};

void MeetingWindow::cb_quit(Address, Address pw){
    reference_to<MeetingWindow>(pw).hide();
}

void MeetingWindow::addPerson(){
    string name = personName.get_string();
    string email = personEmail.get_string();

    personName.clear_value();
    personEmail.clear_value();

    people.push_back(new Person(name, email));
}

void MeetingWindow::cb_new_person(Address, Address pw){
    reference_to<MeetingWindow>(pw).addPerson();
}

void MeetingWindow::printPeople(){
    for(Person* p : people){
        cout << *p << endl;
    }
}

void MeetingWindow::cb_printPeople(Address, Address pw){
    reference_to<MeetingWindow>(pw).printPeople();
}
