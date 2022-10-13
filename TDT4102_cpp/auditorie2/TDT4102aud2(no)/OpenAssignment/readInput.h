#pragma once
#include <iostream>
#include <vector>
#include <string>
#include "Graph.h"

using namespace std;

vector<int> readFromFile(string filename);
//opens a file of ints and puts them in a vector

vector<int> manualInput();
//reads ints from console and puts them in a vector

vector<Graph_lib::Point> intToPoints(vector<int> ints);
//convert list of ints to points. ints.length() % 2 == 0 must be true
