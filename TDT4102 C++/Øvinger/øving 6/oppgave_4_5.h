#pragma once
#include "std_lib_facilities.h"

struct Temps{
    float max;
    float min;
};

istream& operator>>(istream& , Temps&);

void getTempsFromFile(string filename, vector<Temps>& tempsVector);

void drawTempGraph();