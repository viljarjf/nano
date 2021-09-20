#include "std_lib_facilities.h"
#include "oppgave_2.h"

void countLettersOfFile(){
    cout << "Please enter filename: ";
    string filename;
    cin >> filename;
    ifstream ifs {filename+".txt"};
    if(!ifs){
        cout << "Can't open file\n";
        return;
    }
    map<char, int> letters;
    while(!ifs.eof()){
        char c;
        ifs >> c;
        if(c < 'A' || c > 'z'){
            continue;
        }
        else if (!isalpha(c)){
            continue;
        }
        c = tolower(c);
        if (letters.find(c) == letters.end()){
            letters[c] = 0;
        }
        letters[c]++;
    }
    for (auto c : letters){
        cout << c.first << ": " << c.second << endl;
    }
}