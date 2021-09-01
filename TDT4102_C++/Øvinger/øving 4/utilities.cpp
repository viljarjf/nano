#include "utilities.h"
#include "std_lib_facilities.h"
#include <cstdlib>
#include <ctime>

int incrementByValueNumTimes(int startValue, int increment, int numTimes){
    for (int i = 0; i < numTimes; i++) {
        startValue += increment;
    }
    return startValue;
}


void incrementByValueNumTimesRef(int& startValue, int increment, int numTimes){
    for (int i = 0; i < numTimes; i++) {
        startValue += increment;
    }
}

void swapNumbers(int& a, int& b){
    int c = a;
    a = b;
    b = c;    
}

int randomWithLimits(int min, int max){
    int rand_num = rand();
    int diff = max-min;
    return min + (rand_num % diff);
}

void randomizeVector(vector<int>& vec, int n){
    for (int x=0; x<n; x++){
        vec.push_back(randomWithLimits(0,100));
    }
}

void sortVector(vector<int>& vec){
    int i =1;
    int j = i;
    while (i < static_cast<int>(vec.size())){
        j = i;
        while ((j>0) && (vec[j-1] > vec[j])){
            swapNumbers(vec[j], vec[j-1]);
            j--;
        }
        i++;
    }
}

double medianOfVector(vector<int> vec){
    int len = static_cast<int>(vec.size())-1; //-1 pga. 0-indeksering
    if (len%2 == 0){
        return vec[len/2];
    }
    else{
        return (vec[len/2] + vec[len/2 +1]) / 2.0;
    }
}

void printStudent(Student student){
    cout << "Name: " << student.name << endl;
    cout << "Study program: " << student.studyProgram << endl;
    cout << "Age: " << student.age << endl;
}

string randomizeString(int length, char first_possible_char, char last_possible_char){
    string result = "";
    for(int n=0; n<length; n++){
        char letter = randomWithLimits(static_cast<int>(first_possible_char), static_cast<int>(last_possible_char));
        result.push_back(letter);
    }
    return result;
}

string readInputToString(unsigned int length, char first_possible_char, char last_possible_char){
    first_possible_char = toupper(first_possible_char);
    last_possible_char = toupper(last_possible_char);
    bool isLegal = true;
    string input = "";
    do{
        isLegal = true;
        cout << "Enter a string of length " << length << ", where the letters are between " << first_possible_char << " and " << last_possible_char << ": ";
        cin >> input;
        cout << endl;
        for (char c : input){
            if (!isalpha(c) || (input.size() != length)){
                cout << "Illegal input, please retry." << endl;
                isLegal = false;
                break;
            }
            c = toupper(c);
            if ((first_possible_char > c) || (last_possible_char < c)){
                cout << "Illegal input, please retry." << endl;
                isLegal = false;
                break;
            }
        }
    }
    while(!isLegal);

    return input;
}

unsigned int countChar(string s, char c){
    unsigned int count = 0;
    for (char n : s){
        if(n==c){
            count++;
        }
    }
    return count;
}