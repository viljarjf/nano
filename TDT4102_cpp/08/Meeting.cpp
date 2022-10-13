#include "std_lib_facilities.h"
#include "Person.h"
#include "Meeting.h"

set<const Meeting*> Meeting::meetings;

ostream& operator<<(ostream& os, const Campus& c){
    switch (c){
        case Campus::Trondheim:{
            os << "Trondheim";
            break;
        }
        case Campus::Ålesund:{
            os << "Ålesund";
            break;
        }
        case Campus::Gjøvik:{
            os << "Gjøvik";
            break;
        }
        default:
            break;
    }
    return os;
}

Meeting::Meeting(int d, int sT, int eT, Campus loc, string sub, const Person * l):
    day{d}, startTime{sT}, endTime{eT}, location{loc}, subject{sub}, leader{l}
    {
        addParticipants(l);
        meetings.insert(this);
}

Meeting::~Meeting(){
    meetings.erase(this);   
}

int Meeting::getDay() const{
    return day;
}
int Meeting::getStartTime() const{
    return startTime;
}
int Meeting::getEndTime() const{
    return endTime;
}
Campus Meeting::getLocation() const{
    return location;
}
string Meeting::getSubject() const{
    return subject;
}
const Person * Meeting::getLeader() const{
    return leader;
}

void Meeting::addParticipants(const Person* p){
    participants.insert(p);
}

vector<string> Meeting::getParticipants() const{
    vector<string> names;
    for(auto p: participants){
        names.push_back(p->getName());
    }
    return names;
}

ostream& operator<<(ostream& os, const Meeting& m){
    os << "Subject: " << m.getSubject() << endl;
    os << "Location: " << m.getLocation() << endl;
    os << "Start-time: " << m.getStartTime() << endl;
    os << "End-time: " << m.getEndTime() << endl;
    os << "Participants: " << endl;
    for (string n: m.getParticipants()){
        os << "    " << n << endl;
    }
    return os;
}

vector<const Person*> Meeting::findPotentialCoDriving() const{
    vector<const Person*> freeSeatPeople;

    //first, find the potential meetings
    for(auto m : meetings){
        if ((abs(m->getStartTime() - startTime) <= 1) && //starts within 1hr
            (abs(m->getEndTime() - endTime) <= 1) &&  //ends within 1hr
            (m->getLocation() == location) && //same place
            (m->getDay() == day) && //same day
            (m != this) //not the same meeting, since that was a requirement for some reason
        ){
            //then, find people with available seats
            for(auto p : m->participants){
                if (p->hasAvailableSeats()){
                    freeSeatPeople.push_back(p);
                }
            }
        }//auto is not strictly neccessary here, but it is easier 
    }
    return freeSeatPeople;
}