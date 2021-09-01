#pragma once
#include "std_lib_facilities.h"


int incrementByValueNumTimes(int startValue, int increment, int numTimes);

void incrementByValueNumTimesRef(int& startValue, int increment, int numTimes);

void swapNumbers(int& a, int& b);

int randomWithLimits(int min, int max);

void randomizeVector(vector<int>& vec, int n);

void sortVector(vector<int>& vec);

double medianOfVector(vector<int> vec);

struct Student{
    string name;
    string studyProgram;
    int age;
};

void printStudent(Student student);

string randomizeString(int length, char first_possible_char, char last_possible_char);

string readInputToString(unsigned int length, char first_possible_char, char last_possible_char); 

unsigned int countChar(string s, char c);