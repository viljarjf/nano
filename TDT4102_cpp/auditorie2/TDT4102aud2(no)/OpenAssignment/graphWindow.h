#pragma once
#include <vector>
#include "Window.h"
#include "Graph.h"

using namespace Graph_lib;

class GraphWindow{
    Point tl;
    int w;
    int h;
    vector<Point> points;
    Vector_ref<Line> lines;

    public:
        GraphWindow(vector<Point> points, Point tl, int w, int h) : Graph_lib::Window{tl, w, h, "Graphing window"}, points{points} { // why does Window give an error?
            //add code to draw all lines here
        }
};