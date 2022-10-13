#include "MinesweeperWindow.h"

MinesweeperWindow::MinesweeperWindow(Point xy, int width, int height, int mines, const string& title) :
	Graph_lib::Window{xy, width * cellSize, height*cellSize, title}, width{width}, height{height}, mines{mines}
	//Initialiser medlemsvariabler, bruker ogsaa konstruktoren til Windowsklassen
{
	// Legg til alle tiles paa vinduet
	for (int i = 0; i < height; ++i) {
		for (int j = 0; j < width; ++j) {
			int y = i* cellSize,
				x = j * cellSize;
			tiles.push_back(new Tile{ Point{x, y}, cellSize, cb_click });
			attach(tiles.back());
		}
	}

	//Legg til miner paa tilfeldige posisjoner
	for (int n = 0; n < mines; n++){
		int rand = std::rand();
		rand %= (height*width); //create random number in the size range

		if (tiles[rand].getIsMine()){n--; continue;}//skip if there is already a mine there

		tiles[rand].setIsMine(true);
	}

	// Fjern window reskalering
	resizable(nullptr);
	size_range(x_max(), y_max(), x_max(), y_max());
}

int MinesweeperWindow::countMines(vector<Point> points) const {
	int n = 0;
	for (auto p : points){
		if (at(p).getIsMine()){n++;}
	}
	return n;
}

vector<Point> MinesweeperWindow::adjacentPoints(Point xy) const {
	vector<Point> points;
	for (int di = -1; di <= 1; ++di) {
		for (int dj = -1; dj <= 1; ++dj) {
			if (di == 0 && dj == 0) {
				continue;
			}

			Point neighbour{ xy.x + di * cellSize,xy.y + dj * cellSize };
			if (inRange(neighbour)) {
				points.push_back(neighbour);
			}
		}
	}

	return points;
}

void MinesweeperWindow::openTile(Point xy) {
	if (at(xy).getState() == Cell::flagged || at(xy).getState() == Cell::disabled){return;}

	vector<Point> adjPoints = adjacentPoints(xy);
	int adjacentMines = countMines(adjPoints);

	if (at(xy).getState() == Cell::open){
		int flaggedNeighbours = 0;
		for (auto p : adjPoints){
			if (at(p).getState() == Cell::flagged){
				flaggedNeighbours++;
			}
		}
		if (flaggedNeighbours >= adjacentMines && adjacentMines != 0){
			for (auto p : adjPoints){
				if (at(p).getState() == Cell::closed){
					openTile(p);
				}
			}
		}
	}
		
	else{//state = closed
		at(xy).open();

		if (!at(xy).getIsMine()){
			at(xy).setAdjMines(adjacentMines);
			if (adjacentMines==0){
				for (Point p : adjPoints){
					openTile(p);
				}
			}
		}

		else{
			this->set_label("You lost");
			for (auto t : tiles){
				if (t->getIsMine()){
					t->open();
				}
				else{
					t->disable();
				}
			}
		}
	}
}

void MinesweeperWindow::flagTile(Point xy) {
	at(xy).flag();
}

//Kaller opentile ved venstreklikk og flagTile ved hoyreklikk/trykke med to fingre paa mac
void MinesweeperWindow::cb_click(Address, Address pw)
{
	Point xy{ Fl::event_x(),Fl::event_y() };
	MouseButton mb = static_cast<MouseButton>(Fl::event_button());
	auto& win = reference_to<MinesweeperWindow>(pw);

	if (!win.inRange(xy)) {
		return;
	}

	if (win.winCheck()){
			win.set_label("You won!");
			return;
	}

	switch (mb) {
	case MouseButton::left:
		win.openTile(xy);
		break;
	case MouseButton::right:
		win.flagTile(xy);
		break;
	}
	
	win.flush();
}


bool MinesweeperWindow::winCheck() const{
	int openTiles = 0;
	for (auto t : tiles){
		if (t->getState() == Cell::open){
			openTiles++;
		}
	}
	return (openTiles == (width*height)-mines);
}
