#include "fibonacci.h"
#include <iostream>

void fillInFibonacciNumbers(unsigned long long result[], int length){
    for (int n=0; n<length; n++){
        if (n<2){
            result[n]=n;
        }
        else{
            result[n]=result[n-1]+result[n-2];
        }
    }
}

void printArray(unsigned long long arr[], int length){
    for(int n=0; n<length; n++){
        std::cout << arr[n] << "\n";
    }
}

void createFibonacci(){
    std::cout << "Please enter how many Fibonacci numbers you want\n";
    int length=0;
    std::cin >> length;

    unsigned long long* arr = new unsigned long long[length];

    fillInFibonacciNumbers(arr, length);

    printArray(arr, length);

    delete(arr);
}