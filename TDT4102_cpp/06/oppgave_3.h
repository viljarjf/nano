#pragma once
#include "std_lib_facilities.h"

class CourseCatalog{
    map<string, string> courses;
    
    public:
        CourseCatalog();
        friend ostream& operator<<(ostream&, const CourseCatalog&);
        void addCourse(string code, string name);
        void removeCourse(string code);
        string getCourse(string code);
        void saveToFile(string filename);
        void readFromFile(string filename);
};