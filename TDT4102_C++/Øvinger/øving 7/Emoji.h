#pragma once

// Include Graph_lib library files that holds declarations needed for Window,
// and Shape derivatives.
#include "Graph.h"
#include "GUI.h"



using namespace Graph_lib;

// An abstract class. Concrete classes derived from this base class
// has to implement the member function attach_to().
class Emoji
{
public:
	// Disable copying. Disable slicing, etc.
	Emoji(const Emoji&) = delete;
	Emoji& operator=(const Emoji&) = delete;

	// Deleting the copy constructor also deletes the default constructor.
	// Emoji needs a default constructor.
	Emoji() {}
	// Emoji() = default; // is an alternative way of achieving the same.

	// The pure virtual function that has to be overriden for a deriving class
	// to be instantiable. Every class deriving from Emoji is supposed to
	// attach all its Shapes to a window. This makes the class abstract.
	virtual void attach_to(Graph_lib::Window&) = 0;

	// Relevant because Vector_ref can own Emojis and automatically cleans up.
	// Subject will be visited later in the course.
	virtual ~Emoji() {}
};


class Face: public Emoji{
	protected:
		Point c;
		int r;

		Circle face{c, r};

	public:
		Face(const Face&) = delete;
		Face& operator=(const Face&) = delete;

		Face() {}
		Face(Point centre, int radius);

		void attach_to(Graph_lib::Window&) override = 0 ;

		virtual ~Face() {}
};

class EmptyFace: public Face{

	Circle lEye{Point{c.x-15, c.y-20}, 9};
	Circle rEye{Point{c.x+15, c.y-20}, 9};

	Circle lIris{Point{c.x-15, c.y-20}, 13};
	Circle rIris{Point{c.x+15, c.y-20}, 13};

	public:
		EmptyFace(Point centre, int radius);

		void attach_to(Graph_lib::Window&) override;
};

class Smiley: public EmptyFace{
	Arc smile{Point{c.x, c.y-7}, 20, 13, 180, 360};

	public:
		Smiley(Point centre, int radius);

		void attach_to(Graph_lib::Window&) override;
};

class Sad: public Face{
	Circle lEye{Point{c.x-14, c.y}, 9};
	Circle rEye{Point{c.x+16, c.y}, 9};

	Circle lIris{Point{c.x-15, c.y-3}, 13};
	Circle rIris{Point{c.x+15, c.y-3}, 13};

	Arc frown{Point{c.x, c.y+15}, 20, 13, 0, 180};

	public:
		Sad(Point centre, int radius);
		void attach_to(Graph_lib::Window&) override;
};

class Angry: public Face{
	Circle lEye{Point{c.x-15, c.y-10}, 9};
	Circle rEye{Point{c.x+15, c.y-10}, 9};

	Circle lIris{Point{c.x-15, c.y-10}, 13};
	Circle rIris{Point{c.x+15, c.y-10}, 13};

	Arc lEyeBrow{Point{c.x-24, c.y-18}, 40, 20, 0, 60};
	Arc rEyeBrow{Point{c.x+24, c.y-18}, 40, 20, 120, 180};

	Arc frown{Point{c.x, c.y+10}, 20, 10, 0, 180};

	public:
		Angry(Point centre, int radius);
		void attach_to(Graph_lib::Window&) override;
};

class Meh: public Face{
	Circle lEye{Point{c.x-12, c.y-10}, 9};
	Circle rEye{Point{c.x+18, c.y-10}, 9};

	Circle lIris{Point{c.x-10, c.y-10}, 13};
	Circle rIris{Point{c.x+20, c.y-10}, 13};

	Circle mouth{Point{c.x+10, c.y+15}, 7};
	public:
		Meh(Point centre, int radius);
		void attach_to(Graph_lib::Window&) override;
};