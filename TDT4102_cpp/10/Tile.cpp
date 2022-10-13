#include "Tile.h"


// For aa sette Tilelabel i henhold til state
std::map<Cell, string> cellToSymbol{ {Cell::closed, ""},
									 {Cell::open, ""},
									 {Cell::flagged, "@<"} };

//mapet funket ikke når det var const

void Tile::open()
{
	if (state == Cell::closed){
		static_cast<Fl_Button*>(pw)->set();//Setter en button som trykket paa, tilsvarer aapnet rute
		state = Cell::open;

		if (isMine){
			set_label("X");
			set_label_color(Color::red);
		}
	}
	return;
}

void Tile::flag()
{ 
	if (state == Cell::flagged){
		state = Cell::closed;
		set_label("");
	}
	else if (state == Cell::closed){
		state = Cell::flagged;
		set_label("@<");
		set_label_color(Color::blue);
	}
}

void Tile::setAdjMines(int n){
	if (n==0){return;}
	set_label(to_string(n));
	switch (n){
		case 1:
			set_label_color(Color::blue);
			break;
		case 2:
			set_label_color(Color::red);
			break;
		case 3:
			set_label_color(Color::dark_green);
			break;
		case 4:
			set_label_color(Color::dark_magenta);
			break;
		case 5:
			set_label_color(Color::dark_blue);
			break;
		case 6:
			set_label_color(Color::dark_cyan);
			break;
		case 7:
			set_label_color(Color::dark_red);
			break;
		case 8:
			set_label_color(Color::dark_yellow);
			break;
	}
}