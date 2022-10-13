#include <algorithm>
#include <cassert>
#include <map>

#include "GUI.h" // for Simple_window only (doesn't really belong in Window.h)
#include "Graph.h"
#include "Simple_window.h"

using namespace std;
using namespace Graph_lib;


// I denne oppgaven skal du lage en klasse for matematiske vektorer i planet
// (2d, dvs. 2 dimensjoner). En vektor består av to komponenter (tall): x og y.
// Vi bruker notasjonen a = [x, y] for å angi en vektor a med verdier x og y. I
// Figur 1 (se pdf eller Inspera) er det vist to eksempel‐vektorer a og b med
// blått. Vi bruker et vanlig koordinatsystem med origo i nedre venstre hjørne,
// positiv x‐verdi er mot høyre og positiv y‐verdi oppover.



// Oppgave 1a: Deklarer klassen Vector2d med to medlemsvariabler x og y av type
// double. Medlemsvariablene skal være public. Deklarer og implementer
// konstruktøren inline.
class Vector2d{
  public:
      double x;
      double y;
      Vector2d(double X, double Y) : x{X}, y{Y} {}
      Vector2d(): x{0}, y{0} {} //default konstruktør, måtte til for å kjøre koden
      double length();
      Vector2d operator*(double k);
};


// Oppgave 1b:  Lengden til en vektor er definert som sqrt(x2 + y2 ) der sqrt()
// er en funksjon i standardbiblioteket for å beregne kvadratrot. Implementer en
// medlemsfunksjon Vector2d::length() som returnerer lengden.
#include <cmath>

double Vector2d::length(){
    return (std::sqrt(x*x+y*y));
}


// Oppgave 1c: Addisjon av vektorer gjøres komponentvis og resultatet er en ny
// vektor. Hvis vektorene [x0, y0] og [x1, y1] adderes så blir resultatet
// vektoren [x0 + x1, y0 + y1]. Dette er vist i Figur 1 (se pdf eller Inspera)
// der den røde pilen er vektoren c = a + b. Implementer operator+ for addisjon
// av objekter fra klassen Vector2d.
// Operatoren skal returnere summen av to vektorer, og skal implementeres
// utenfor klassen (altså ikke være medlemsoperator).

Vector2d operator+(Vector2d& v1, Vector2d& v2){
    double x = v1.x + v2.x; //lovlig siden x og y er public
    double y = v1.y + v2.y;
    return *new Vector2d(x, y);
}

// Oppgave 1d: En vektor kan multipliseres med en konstant (skalar), dvs. [x, y]
// * k . Resultatet blir en ny vektor [x * k, y * k]. Implementer operator* for
// å kunne utføre slik multiplikasjon der [x,y] er et Vector2D objekt og k er av
// type double. Operatoren skal implementeres som medlemsoperator.

Vector2d Vector2d::operator*(double k){
    x *= k;
    y *= k;
    return *this;
}


// Oppgave 1e: Definer (implementer) overlasting (Eng. overloading) av
// utskriftsoperatoren operator<< for et objekt fra klassen Vector2d . Formatet
// skal være [x, y]. Vi bryr oss ikke om presisjon/antall desimaler.
// Deklarasjonen ser slik ut: ostream & operator<<(ostream& out, const Vector2d&
// v)

#include <vector>
ostream& operator<<(ostream& out, const Vector2d& v){
    //antar get-funksjonene er const
    return out << "[" << v.x << ", " << v.y << "]";
}


// Oppgave 1f: Skriv en funksjon vectorSum(const vector<Vector2d>& vectors) som
// returnerer et Vector2d objekt som er summen av alle vektorene i vectors.

Vector2d vectorSum(const vector<Vector2d>& vectors){
    double x = 0;
    double y = 0;
    for(auto v : vectors){
        x += v.x;
        y += v.y;
        //på denne måten slipper vi å definere = og/eller +=
    }
    return *new Vector2d(x, y);
}


constexpr int win_W = 500;
constexpr int win_H = 500;
// *************************************************************** Graphic demo
// code for testing only
void addVector(vector<Shape *> &drawing, const Vector2d &vec, const Color col) {
  if ((vec.x > 10.0) || (vec.y > 10.0))
    throw "too large x or y in Vector2d object, ignored";

  Line *linePtr = new Line{{0, win_H},
                           {static_cast<int>((vec.x * win_W) / 10.0),
                            static_cast<int>(win_H - (vec.y * win_H) / 10.0)}};
  linePtr->set_color(col);
  drawing.push_back(linePtr);
}

void showDrawing(Simple_window &win, vector<Shape *> &drawing) {
  if (drawing.empty()) {
    throw "drawing vector must be non-empty";
  }

  for (auto s : drawing)
    win.attach(*s);
}

void draw(Simple_window &win, vector<Shape *> &shapes, Color col) {
  if (shapes.empty()) {
    throw "shapes vector must be non-empty";
  }

  for (auto s : shapes) {
    s->set_color(col);
    win.attach(*s);
  }
}

struct doublePoint {
  double x;
  double y;
};

void addLine(vector<Shape *> &s, const doublePoint from, const doublePoint to) {
  if ((from.x < 0.0) || (from.y < 0.0) || (to.x < 0.0) || (to.y < 0.0)) {
    cerr << "addLine: negative x or y in Vector2d object, ignored.\n";

    return;
  }
  if ((from.x > 10.0) || (from.y > 10.0) || (to.x > 10.0) || (to.y > 10.0)) {
    cerr << "addLine: too large x or y in Vector2d object, ignored.\n";
    return;
  }

  Line *linePtr = new Line{{static_cast<int>((from.x * win_W) / 10.0),
                            static_cast<int>(win_H - (from.y * win_H) / 10.0)},
                           {static_cast<int>((to.x * win_W) / 10.0),
                            static_cast<int>(win_H - (to.y * win_H) / 10.0)}};
  s.push_back(linePtr);
}

vector<Shape *> makeTrack(const vector<Vector2d> &vectors) {
  vector<Shape *> sVec;
  doublePoint from{0.0, 0.0};
  for (auto v : vectors) {
    doublePoint to = {from.x + v.x, from.y + v.y};
    addLine(sVec, from, to);
    from = to;
  }
  return sVec;
}

void emptyDrawing(Simple_window &win, vector<Shape *> &v) {
  while (v.size() > 0) {
    win.detach(*v.at(v.size() - 1));
    delete v.at(v.size() - 1);
    v.pop_back();
  }
}

// Oppgave 1g: Vi skal nå bruke en STL‐vector av Vector2d ‐objekter for å
// representere et spor i planet. Sporet kan f.eks. være fra en robot, fra et
// forsøksdyr eller en jogger, og må være innenfor området (0.0, 0.0) til
// (10.0, 10.0) (sporingsområdet). I Figur 2 (se pdf eller Inspera) viser den
// sorte streken et spor som starter i koordinat‐posisjon (0.0, 0.0) og er
// representert med vector<Vector2d> track = {{1.0, 0.5}, {2.0, 0.0},
// {1.0, 1.0}, {‐1.0, 2.0}, {‐1.0, 0.0}, {‐1.0, ‐1.0}}; Sporet består av 6
// linjestykker, hver representert ved et Vector2d ‐objekt. Posisjonene etter
// hver forflytning er angitt med røde tall nr. 1, 2, 3 ... til og med 6 som er
// sluttposisjon i dette tilfellet. Vi kan tenke oss at måleenheten er kilometer
// (km) og at joggerens klokke lagrer posisjonen ved hvert 10 minutt. Som et
// eksempel har vi vist med den grønne pilen at joggeren er ved posisjon (3.0,
// 0.5) etter 20 minutter. (Husk at hvert element i track bare gir
// forflyttningen de siste 10 minutter, og ikke posisjonen). Skriv en funksjon
// void trackStats(const vector<Vector2d>& track) som rapporterer lengden på
// joggeturen i km med 2 desimaler etter punktum, maksimal‐hastigheten i hele
// meter pr minutt for turen, og sluttposisjon relativt til startpunktet. For
// sporet i figur 2 (se pdf eller Inspera) vil utskriften bli slik: Length: 9.18
// km, max‐speed: 224 m/min, ended at [1, 2.5]

#include "stdio.h"
#include <iomanip>

void trackStats(const vector<Vector2d>& track){
    double len = 0;
    double max_speed = 0;
    Vector2d final_pos;
    for (auto v: track){
        //finner lengden av segmentet
        double curr_len = v.length(); 
        //finner farten i segmentet. km/10 min = m*100
        double curr_speed = curr_len*100; 
        len += curr_len; 
        //oppdaterer max_speed hvis nødvendig
        max_speed = (curr_speed > max_speed ? curr_speed : max_speed); 
        //oppdaterer posisjonen
        final_pos = final_pos + v;
    }
    std::cout << "Length: " << std::setprecision(2) << len << " km,";
    std::cout << " max-speed: " << std::setprecision(0) << max_speed << " m/min,";
    std::cout << " ended at " << final_pos;
}

struct Clean {
  Vector2d currentPos;

  // constructor will initialize current pos correctly
  Clean()
      : currentPos{0.0, 0.0} {
  }

  Vector2d operator()(Vector2d delta) {
    Vector2d np = currentPos + delta;
    if ((np.x < 0.0) || (np.x > 10.0) || (np.y < 0.0) || (np.y > 10.0)) {
      return {0.0, 0.0};
    } else {
      currentPos = np;
      return delta;
    }
  }
};

// Oppgave 1h: Vi ønsker å erstatte de elementer i vektoren som ville føre til
// en posisjon utenfor sporingsområdet med en null‐vektor, Figur 2. dvs. et
// Vector2d ‐objekt med verdi {0.0, 0.0}. Skriv en funksjon cleanTrack () som
// tar inn en referanse til et spor og gjør denne operasjonen element for
// element. For å få full score på denne oppgaven skal du bruke transform fra
// <algorithm> med et funksjons‐objekt. Deklarasjonen for transform er vist i
// vedlegget. Andre løsninger kan også gi poeng.

#include <algorithm>

//lager operasjonen som skal utføres
Vector2d limitVector(Vector2d v){
    double x = 0;
    double y = 0;
    //skjekk at posisjonen er lovlig
    if ((v.x > 0) &&
        (v.x < 10) &&
        (v.y > 0) &&
        (v.y < 10)){
            x = v.x;
            y = v.y;
        }
    return *new Vector2d(x, y);
}

vector<Vector2d> cleanTrack(vector<Vector2d>& track){
    //lag en tom vektor med vektorer
    vector<Vector2d> legalTrack;
    legalTrack.resize(track.size());
    
    // skaff en lovlig track med transform
    std::transform(track.begin(), track.end(), legalTrack.begin(), limitVector);
    
    return legalTrack;
}

void printTrack(const vector<Vector2d> track) {
  cout << "Track is: ";
  for (auto elt : track)
    cout << " " << elt;
  cout << endl;
}

void plotTrack(Simple_window &win, const vector<Vector2d> &track, Color col) {
  vector<Shape *> t = makeTrack(track);
  draw(win, t, col);
}

int main() {

  cout << "Tracking based on Vector2d from exam May 2019\n";

  Point tl{100, 100};
  Simple_window win{tl, win_W, win_H, "Tracking"};

  const Vector2d a{3.0, 2.0};
  const Vector2d b{2.0, 6.0};
  vector<Vector2d> vectors{a, b};

  vector<Vector2d> track{{1.0, 0.5},  {2.0, 0.0},  {1.0, 1.0},
                         {-1.0, 2.0}, {-1.0, 0.0}, {-1.0, -1.0}};
  plotTrack(win, track, Color::black); // For 5 in exam text
  trackStats(track);
  win.wait_for_button();

  vector<Vector2d> track2{
      {1.0, 1.5}, {-2.0, 1.0}, {3.0, 12.0}, {1.0, -8.0}, {-1.0, 0.0}};

  cout << "\ntrack2:\n";
  printTrack(track2);
  plotTrack(win, track2, Color::blue);
  win.wait_for_button();
  cleanTrack(track2);
  printTrack(track2);
  plotTrack(win, track2, Color::green);
  win.wait_for_button();
  cout << "\ntrack3:\n";

  vector<Vector2d> track3{
      {3.0, 9.0}, {2.0, 0.0}, {8.0, 0.0}, {-2.0, 2.0}, {-1.0, -1.0}};
  printTrack(track3);
  plotTrack(win, track3, Color::dark_red);
  win.wait_for_button();
  cleanTrack(track3);
  printTrack(track3);
  plotTrack(win, track3, Color::cyan);
  win.wait_for_button();

  return 0;
}
