#include "iterators.h"
#include <iostream>
#include <iterator>
#include <algorithm>



void printVector(vector<string> vec){
    vector<string>::iterator itr;
    for (itr = vec.begin(); itr < vec.end(); itr++){
        cout << *itr << endl;
    }
}

void printReverseVector(vector<string> vec){
    reverse_iterator<vector<string>::iterator> ritr;
    for (ritr = vec.rbegin(); ritr < vec.rend(); ritr++){
        cout << *ritr << endl;
    }
}

void replace(vector<string>& vec, string old, string replacement){
    vector<string>::iterator itr;
    for (itr = vec.begin(); itr < vec.end(); itr++){
        if (*itr == old){
            *itr = replacement;
        }
    }
}

void printSet(set<string> s){
    set<string>::iterator itr;
    for (itr = s.begin(); itr != s.end(); itr++){
        cout << *itr << endl;
    }
}

void printReverseSet(set<string> s){
    reverse_iterator<set<string>::iterator> ritr;
    for (ritr = s.rbegin(); ritr != s.rend(); ritr++){
        cout << *ritr << endl;
    }
}

void replace(set<string>& s, string old, string replacement){
    if (s.find(old) != s.end()){
        s.erase(old);
        s.insert(replacement);
    }
}

