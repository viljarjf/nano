#pragma once
#include "std_lib_facilities.h"
#include "Meeting.h"
#include "Person.h"
#include "Graph.h"
#include "Window.h"
#include "GUI.h"


using namespace Graph_lib;

class MeetingWindow: public Window{

    static constexpr int pad = 50;
    static constexpr int btnW = 100;
    static constexpr int btnH = 50;
    static constexpr int fieldW = 200;
    static constexpr int fieldH = 50;
    static constexpr int fieldPad = 65;

    static constexpr Point quitBtnAnchor{fieldW+fieldPad*2, pad};
    static constexpr Point personNameAnchor{fieldPad, pad};
    static constexpr Point personEmailAnchor{fieldPad, 2*pad+fieldH};
    static constexpr Point personNewBtnAnchor{fieldPad, 3*pad+2*fieldH};
    static constexpr Point printPeopleBtnAnchor{fieldW+fieldPad*2, 2*pad+btnH};

    Button quitBtn;
    In_box personName;
    In_box personEmail;
    
    Vector_ref<Person> people;
    Button personNewBtn;

    Button printPeopleBtn;

    public:
        MeetingWindow(Point xy, int w, int h, const string& title);           

            static void cb_quit(Address, Address pw);
            void addPerson();
            static void cb_new_person(Address, Address pw);
            void printPeople();
            static void cb_printPeople(Address, Address pw);
};