#include "Emoji.h"

using namespace Graph_lib;

Face::Face(Point centre, int radius):
c{centre}, r{radius}, face{Circle{centre, radius}} {
    face.set_fill_color(Color::yellow);
}

void Face::attach_to(Graph_lib::Window& win){
    win.attach(face);
}

EmptyFace::EmptyFace(Point centre, int radius) : Face(centre, radius) {
    lEye.set_fill_color(Color::black);
    lEye.set_color(Color::black);
    rEye.set_fill_color(Color::black);
    rEye.set_color(Color::black);

    lIris.set_fill_color(Color::white);
    rIris.set_fill_color(Color::white);
}

void EmptyFace::attach_to(Graph_lib::Window& win){
    win.attach(face);
    win.attach(lIris);
    win.attach(rIris);
    win.attach(lEye);
    win.attach(rEye);
}

Smiley::Smiley(Point centre, int radius) : EmptyFace(centre, radius) {
    smile.set_color(Color::black);
}

void Smiley::attach_to(Graph_lib::Window& win){
    EmptyFace::attach_to(win);
    win.attach(smile);
}

Sad::Sad(Point centre, int radius) : Face(centre, radius) {
    lEye.set_fill_color(Color::black);
    lEye.set_color(Color::black);
    rEye.set_fill_color(Color::black);
    rEye.set_color(Color::black);

    lIris.set_fill_color(Color::white);
    rIris.set_fill_color(Color::white);

    frown.set_color(Color::black);
}

void Sad::attach_to(Graph_lib::Window& win){
    win.attach(face);
    win.attach(lIris);
    win.attach(rIris);
    win.attach(lEye);
    win.attach(rEye);
    win.attach(frown);
}

Angry::Angry(Point centre, int radius) : Face(centre, radius) {
    lEye.set_fill_color(Color::black);
    lEye.set_color(Color::black);
    rEye.set_fill_color(Color::black);
    rEye.set_color(Color::black);

    lIris.set_fill_color(Color::white);
    rIris.set_fill_color(Color::white);

    lEyeBrow.set_color(Color::black);
    rEyeBrow.set_color(Color::black);

    frown.set_color(Color::black);
    frown.set_fill_color(Color::red);
}

void Angry::attach_to(Graph_lib::Window& win){
    win.attach(face);
    win.attach(lIris);
    win.attach(rIris);
    win.attach(lEye);
    win.attach(rEye);
    win.attach(lEyeBrow);
    win.attach(rEyeBrow);
    win.attach(frown);
}
Meh::Meh(Point centre, int radius) : Face(centre, radius) {
    lEye.set_fill_color(Color::black);
    lEye.set_color(Color::black);
    rEye.set_fill_color(Color::black);
    rEye.set_color(Color::black);

    lIris.set_fill_color(Color::white);
    rIris.set_fill_color(Color::white);

    mouth.set_color(Color::black);
    mouth.set_fill_color(Color::black);
}

void Meh::attach_to(Graph_lib::Window& win){
    win.attach(face);
    win.attach(lIris);
    win.attach(rIris);
    win.attach(lEye);
    win.attach(rEye);
    win.attach(mouth);
}