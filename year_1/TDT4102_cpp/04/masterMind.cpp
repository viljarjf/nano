#include "std_lib_facilities.h"
#include "masterMind.h"
#include "utilities.h"
#include "masterVisual.h"

void playMasterMind(){
    constexpr int size = 4;
    constexpr int letters = 6;
    constexpr int attempts = 10;
    string guess;
    bool win = false;

    string code = randomizeString(size, 'A', 'A'+(letters-1));

    MastermindWindow mwin{Point{900, 20}, winW, winH, "Mastermind"};
    addGuess(mwin, code, size, 'A', 0);
    hideCode(mwin, size);

    cout << "Colors: A = red, B = green, C = yellow, D = blue, E = lilac, F = cyan" << endl;
    cout << "A black dot means one of the guesses were of the correct color and in the correct position" << endl;
    cout << "A white dot means one of the guesses were of the correct color" << endl;

    for (int attempt = 1; attempt <= attempts; attempt++){
        guess = mwin.getInput(size, 'A', 'A'+(letters-1));
        addGuess(mwin, guess, size, 'A', attempt);
        addFeedback(mwin, checkCharactersAndPosition(guess, code), checkCharacters(guess, code), size, attempt);
        cout << "----------------------------\n";
        if (checkCharactersAndPosition(guess, code) == size){
            win = true;
            break;
        }
        cout << attempts-attempt << " attempts left." << endl;
    }
    if (win){
        cout << "Congratulations! You guessed the code!" << endl;
    }
    else{
        cout << "You lost. Too bad. The correct code was " << code << "." << endl;
    }
}

int checkCharactersAndPosition(string input, string secret){
    int correct = 0;
    for(int x = 0; x < secret.size(); x++){
        if (input[x] == secret[x]){
            correct++;
        }
    }
    return correct;
}

int checkCharacters(string input, string secret){
    int correct = 0;
    for (auto s : input){
        if (find(begin(secret), end(secret), s) != end(secret)){
            correct++;
        }
    }
    return correct;
}