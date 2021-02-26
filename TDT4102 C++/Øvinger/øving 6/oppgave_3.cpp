#include "std_lib_facilities.h"
#include "oppgave_3.h"

CourseCatalog::CourseCatalog() : courses{} {}

ostream& operator<<(ostream& os, const CourseCatalog& cc){
    for (auto c : cc.courses){
        os << c.first << " " << c.second<< endl;
    }
    return os;
}

void CourseCatalog::addCourse(string code, string name){
    courses[code] = name;
}

void CourseCatalog::removeCourse(string code){
    courses.erase(code);
}

string CourseCatalog::getCourse(string code){
    return courses[code];
}

void CourseCatalog::saveToFile(string filename){
    ofstream ofs {filename+".txt"};
    if(!ofs){
        cout << "Can't open file\n";
        return;
    }
    int x=1;
    for (auto c : courses){
        ofs << setw(7) << c.first << " | " << c.second;
        if (x != courses.size()){
            ofs << endl;
        }
        x++;
    }
    //ofs << *this;
}

void CourseCatalog::readFromFile(string filename){
    ifstream ifs {filename+".txt"};
    if(!ifs){
        cout << "Can't open file\n";
        return;
    }
    while(!ifs.eof()){
        string line;
        getline(ifs, line);
        string code = line.substr(0, line.find('|')-1);
        string name = line.substr(line.find('|')+2, line.size());
        CourseCatalog::addCourse(code, name);
    }

}