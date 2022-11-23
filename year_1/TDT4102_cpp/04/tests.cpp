#include "tests.h"
#include "std_lib_facilities.h"
#include "utilities.h"

void testCallByValue() {
    int v0 = 5;
    int increment = 2;
    int iterations = 10;
    int result = incrementByValueNumTimes(v0, increment, iterations);
    cout << "v0: " << v0
        << " increment: " << increment
        << " iterations: " << iterations
        << " result: " << result << endl;
}

void testCallByRefrence(){
    int v0 = 5;
    int increment = 2;
    int iterations = 10;
    incrementByValueNumTimesRef(v0, increment, iterations);
    cout << "v0: " << v0
        << " increment: " << increment
        << " iterations: " << iterations;
}

void testVectorSorting(){
    vector<int> percentages;
    randomizeVector(percentages, 30);
    cout << "Random vector, where each element is in [0, 100]:\n";
    for (int x=0; x < static_cast<int>(percentages.size()); x++){
        cout << setw(4) << percentages[x];
    }
    cout << "Median (assuming the vector is sorted): " << medianOfVector(percentages) << endl;
    cout << endl;
    cout << "Swapping the first two numbers with swapNumbers...\n";
    swapNumbers(percentages[0], percentages[1]);
    for (int x=0; x < static_cast<int>(percentages.size()); x++){
        cout << setw(4) << percentages[x];
    }
    cout << endl;
    cout << "Sorting the vector with insertion sort...\n";
    sortVector(percentages);
    for (int x=0; x < static_cast<int>(percentages.size()); x++){
        cout << setw(4) << percentages[x];
    }
    cout << "Median (assuming the vector is sorted): " << medianOfVector(percentages) << endl;
    cout << endl;
}

void testString(){
    string grades = randomizeString(8, 'A', 'G');
    cout << grades << endl;
    vector<int> gradeCount;
    for (char c : "FEDCBA"){
        gradeCount.push_back(countChar(grades, c));
    }
    int sum = 0;
    for(int x = 0; x < gradeCount.size(); x++){
        sum += gradeCount[x]*x;
    }
    cout << "Average grade " << sum/6.0 << endl;
}