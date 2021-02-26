#include "std_lib_facilities.h"
#include "oppgave_1.h"

void writeToFile(){
    cout << "Please enter filename: ";
    string filename;
    cin >> filename;
    ofstream ofs {filename+".txt"};
    if(!ofs){
        cout << "Can't open file\n";
        return;
    }
    else{
        string word;
        cout << "Every word you write will be saved as a separate line in the file\n";
        cout << "Exit by writing \"quit\".\n";
        while (true){
            string word;
            cin >> word;
            if (word == "quit"){
                break;
            }
            if (cin){
                ofs << word << endl;
            }
            else{
                break;//break if input is somehow bad
            }
        }
        
    }
    cin.ignore(2000, '\n');
}

void createFileCopyWithLineNumber(){
    cout << "Please enter filename: ";
    string filename;
    cin >> filename;
    ifstream ifs {filename+".png"};
    if(!ifs){
        cout << "Can't open file\n";
        return;
    }
    ofstream ofs {filename+"_copy.txt"};

    int currentLine=0;
    while (!ifs.eof()){
        currentLine++;
        string line;
        getline(ifs, line);
        ofs << currentLine << ".    " << line << endl;
    }
}
