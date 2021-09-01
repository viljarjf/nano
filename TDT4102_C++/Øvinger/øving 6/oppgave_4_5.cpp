#include "std_lib_facilities.h"
#include "oppgave_4_5.h"
#include "Graph.h"
#include "Simple_window.h"


istream& operator>>(istream& is, Temps& t){
    is >> t.max >> t.min;
    return is;
}

void getTempsFromFile(string filename, vector<Temps>& tempsVector){
    ifstream ifs {filename+".txt"};
    if(!ifs){
        cout << "Can't open file\n";
        return;
    }
    while(!ifs.eof()){
        Temps t;
        ifs >> t;
        tempsVector.push_back(t);
    }
}

void drawTempGraph(){
    vector<Temps> tempsVec;
    getTempsFromFile("temperatures", tempsVec);

    using namespace Graph_lib;    

    //endre disse etter smak
    const int width=1000; //bredden på vinduet
    const int height= 700; //høyden
    int padX=50; //avstanden fra kanten til aksene. pga tekstbredde er den minst 30
    padX = (padX<30) ? 30 : padX;
    const int padY=50;
    const int yAxisNotches=12;  //antall streker på y-aksen
    const int notchInterval = 5; //verdidifferansen mellom hver strek på y-aksen
    

    Point origo {padX, 3*height/5};//60% over x-aksen, 40% under
    Simple_window win {Point{100, 100}, width, height, "Daglige maks- og min-temperaturer fra 3. februar 2018 til og med 3. februar 2019"};


    //Her begynner den stygge koden. mye rar matte i punkter og slikt. Det gir et greit sluttresultat, men det er ikke mye å hente fra å lese det
    //som står ikke i Point. Den generelle strukturen utenom det som står i Point burde være grei


    Axis y_axis { Axis::Orientation::y, Point{origo.x, origo.y+2*(height-2*padY)/5}, (height-2*padY), (yAxisNotches%2==0 ? yAxisNotches-1: yAxisNotches), "Temp [C]"};
    y_axis.set_color(Color::black);
    win.attach(y_axis);

    Axis x_axis { Axis::Orientation::x, origo, width-2*padX, 12};
    x_axis.set_color(Color::black);
    win.attach(x_axis);

    Vector_ref<Text> yAxisLabels;
    for(int i=(-2*yAxisNotches)/5; i<3*yAxisNotches/5+1; i++){
        yAxisLabels.push_back(new Text{ Point{origo.x-25, (origo.y-(i*(height-2*padY)/(yAxisNotches))+5)}, to_string(i*notchInterval)});
        yAxisLabels[yAxisLabels.size()-1].set_color(Color::black);
        win.attach(yAxisLabels[yAxisLabels.size()-1]);
    }

    //x-axis labels must be re-written for other time-formats, this is hard-coded for feb-feb
    const vector<string> months{"jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"};
    Vector_ref<Text> xAxisLabels;
    for(int i=0; i<12; i++){
        string label = months[(i+1)%12];
        xAxisLabels.push_back(new Text{Point{origo.x+(2*i+1)*(width-2*padX)/24-(4*static_cast<int>(label.size())), origo.y+25}, label});
        xAxisLabels[xAxisLabels.size()-1].set_color(Color::black);
        win.attach(xAxisLabels[xAxisLabels.size()-1]);
    }


    Open_polyline max;
    Open_polyline min;

    for(int i=0; i<tempsVec.size(); i++){
        max.add(Point{static_cast<int>(origo.x + i*(width-2*padX)/tempsVec.size()), static_cast<int>(origo.y-tempsVec[i].max*(height-2*padY)/(notchInterval*yAxisNotches))});
        min.add(Point{static_cast<int>(origo.x + i*(width-2*padX)/tempsVec.size()), static_cast<int>(origo.y-tempsVec[i].min*(height-2*padY)/(notchInterval*yAxisNotches))});
    }
    max.set_color(Color::red);
    min.set_color(Color::blue);

    win.attach(max);
    win.attach(min);

    win.wait_for_button();    
}