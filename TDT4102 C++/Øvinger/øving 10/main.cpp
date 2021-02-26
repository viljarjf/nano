#include "MinesweeperWindow.h"
#include "time.h"

int main()
{
	std::cout << "Enter size, on a scale from 1 (small) to 5 (large): ";
	int userSize;
	std::cin >> userSize;
	userSize = (userSize+1)*5; // 10*10 for 1, 30*30 for 5

	std::cout << "Enter difficulty, on a scale from 1 (easy) to 6 (hard): ";
	int difficulty;
	std::cin >> difficulty;

	int userMines = userSize*userSize * difficulty / 20; // difficulty*10% amount of mines

	std::srand(static_cast<unsigned int>(std::time(nullptr))); //seed the rng
	Fl::background(200, 200, 200);
	const int width = userSize;
	const int height = userSize;
	const int mines = userMines;

	Point startPoint{ 200,300 };
	MinesweeperWindow mw{ startPoint, width, height, mines, "Minesweeper" };
	return gui_main();

}
 