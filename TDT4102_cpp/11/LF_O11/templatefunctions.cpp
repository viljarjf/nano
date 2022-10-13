#include <cstdlib>
#include <ctime>
#include <iostream>
#include <string>
#include <vector>
using namespace std;

template<typename T>
void shuffle(vector<T>& vec){
	for (size_t i = 0; i < vec.size() - 1; i++){
      int j = rand() % (vec.size()- i);
      swap(vec[i], vec[i+j]);
	}
}

template<typename T>
T maximum(T a, T b){
	if (b < a){
		return a;
	}
    return b;
}


void testTemplateFunctions(){
	srand(time(nullptr));

	cout << "maximum(1, 2) = " << maximum(1, 2) << '\n';
	cout << "maximum(1.0, 2.3) = " << maximum(1.0, 2.3) << '\n';
	cout << "maximum('X', 'Y') = " <<maximum('X', 'Y') << '\n';
	cout << "maximum(string(\"tre\"), string(\"fire\")) = " << maximum(string("tre"), string("fire")) << '\n';


	vector<int> a{1,2,3,4,5,6,7};
	shuffle(a);
    for (auto x : a) {
		cout << x << " ";
	}
	cout << '\n';

	vector<double> b{1.1, 2.2, 3.3, 4.4};
	shuffle(b);
  for (auto x : b) {
		cout << x << " ";
	}
	cout << '\n';

	vector<string> c{"one", "two", "three", "four"};
	shuffle(c);
	for (const auto& x : c){
		cout << x << " ";
	}
	cout << "\n\n";


}
