#include <iostream>
#include <string>
#include <vector>
#include <set>
using namespace std;

void replace(vector<string> &vec, const string& old, string replacement){
  // it has type vector<string>::iterator
	for(auto it = vec.begin(); it != vec.end(); ++it){	//Iterates through the vector
		if(*it == old){				//When a matching string is found
			it = vec.erase(it);		//it is erased
			it = vec.insert(it, replacement);	//and the new string is inserted at the current position
		}
	}
}

void replace(set<string>& s, const string& old, string replacement) {
  // it has type set<string>::iterator
	for(auto it = s.begin(); it != s.end(); ++it){	//Iterates through the set
		if(*it == old){				//When a matching string is found
			it = s.erase(it);		//it is erased
			it = s.insert(it, replacement);	//and the new string is inserted at the current position
		}
	}
}

void iterators_vec(){
	vector<string> v;
	v.push_back("C++");
	v.push_back("and");
	v.push_back("iterators");
	v.push_back("are");
	v.push_back("power");

  // vit has type vector<string>::iterator
	for (auto vit = v.begin(); vit != v.end(); ++vit)
		cout << *vit << " ";
	cout << '\n';

  // rit has type vector<string>::reverse_iterator
	for (auto rit=v.rbegin(); rit != v.rend(); ++rit){
		cout << *rit << " ";
	}
	cout << '\n';

	replace(v, "are", "is");

	for (auto rit=v.rbegin(); rit < v.rend(); ++rit ){
		cout << *rit << " ";
	}
	cout << '\n';

}

void iterators_set() {
  set<string> s;
  s.insert("Lorem");
  s.insert("Ipsum");
  s.insert("Dolor");
  s.insert("Sit");
  s.insert("Amet");

  // sit has type set<string>::iterator
	for (auto sit = s.begin(); sit != s.end(); ++sit)
		cout << *sit << " ";
	cout << '\n';

  // rit has type set<string>::reverse_iterator
	for (auto rit=s.rbegin(); rit != s.rend(); ++rit){
		cout << *rit << " ";
	}
	cout << '\n';

	replace(s, "Lorem", "Latin");

	for (auto rit=s.rbegin(); rit != s.rend(); ++rit){
		cout << *rit << " ";
	}
	cout << '\n';
}
