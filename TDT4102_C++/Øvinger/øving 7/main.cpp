#include "oppgave_1.h"
#include "Simple_window.h"
#include "Emoji.h"

// Size of window and emoji radius
constexpr int xmax = 1000;
constexpr int ymax = 600;
constexpr int emojiRadius = 50;

int main()
{
	using namespace Graph_lib;

	const Point tl{100, 100};
	const string win_label{"Emoji factory"};
	Simple_window win{tl, xmax, ymax, win_label};

	EmptyFace test(Point{200, 200}, emojiRadius);
	test.attach_to(win);

	Smiley s{Point{350, 200}, emojiRadius};
	s.attach_to(win);

	Sad sad{Point{500, 200}, emojiRadius};
	sad.attach_to(win);

	Angry a{Point{650, 200}, emojiRadius};
	a.attach_to(win);

	Meh m{Point{800, 200}, emojiRadius};
	m.attach_to(win);

	win.wait_for_button();
	testAnimal();
	keep_window_open();
}
