/*
pythonkode:

def isFibonacciNumber(n):
	a=0
	b=1
	while b<n:
		temp=b
		b+=a
		a=temp
	return b==n
*/

#include "std_lib_facilities.h"

int maxOfTwo(int a, int b){
	if (a>b){
		cout << "A is greater than B" << endl;
		return a;
	}
	else{
		cout << "B is greater than A" << endl;
		return b;
	}
}

int fibonacci(int n){
	int a = 0;
	int b = 1;
	int temp;
	cout << "Fibonacci numbers:" << endl;
	for (int x=1; x < (n+1); x++){
		cout << x << " " << b << endl;
		temp = b;
		b += a;
		a = temp;
	}
	cout << "----" << endl;
	return b;
}

int squareNumberSum(int n){
	int totalSum = 0;
	for (int i=0; i<n; i++){
		totalSum += i*i;
		cout << i*i << endl;
	}
	cout << totalSum << endl;
	return totalSum;
}

void triangleNumbersBelow(int n){
	cout << endl;
	int acc = 1;
	int num = 2;
	cout << "Triangle numbers below " << n << ":" << endl;
	while (acc < n){
		cout << acc << endl;
		acc += num;
		num++;
	}
	cout << endl;
	return;
}

bool isPrime(unsigned int n){
	for (unsigned int j=2; j<n; j++){
		if (n%j==0){
			return false;
		}
	}
	return true;
}

void naivePrimeNumberSearch(int n){
	for (int number=2; number<n; number++){
		if (isPrime(number)){
			cout << number << " is prime" << endl;
		}
	}
}

int findGreatestDivisor(int n){
	for (int divisor=(n-1); divisor>0; divisor -=1){
		if (n%divisor == 0){
			return divisor;
		}
	}
	return 0;
}

int main(){
	cout << "Oppgave a)\n";
	cout << maxOfTwo(5, 6) << endl;
	cout << endl;

	cout << "Oppgave c)\n";
	cout << fibonacci(10) << endl;
	cout << endl;

	cout << "Oppgave d)\n";
	cout << squareNumberSum(4) << endl;
	cout << endl;

	cout << "Oppgave e)\n";	
	triangleNumbersBelow(10);
	cout << endl;

	cout << "Oppgave f)\n";
	cout << "Er 1048573 primtall? " << isPrime(1048573) << endl; 
	cout << "Er 10485730 primtall? " << isPrime(10485730) << endl; 
	cout << endl;

	cout << "Oppgave g)\n";
	naivePrimeNumberSearch(16);
	cout << endl;

	cout << "Oppgave h)\n";
	cout << findGreatestDivisor(183) << endl;
	cout << endl;

	keep_window_open();
}