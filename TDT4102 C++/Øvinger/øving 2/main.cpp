#include "std_lib_facilities.h"
#include "Graph.h"
#include "Simple_window.h"

//1a
void inputAndPrintInteger(){
	int x;
	cout << "Skriv inn et tall ";
	cin >> x;
	cout << "\nDu skrev inn " << x << endl;
	return;
}

//1b
int inputInteger(){
	int x;
	cout << "Skriv inn et tall ";
	cin >> x;
	return x;
}

//1c
void inputIntegersAndPrintSum(){
	int a{inputInteger()}; //bruker inputInteger siden da får jeg verdien av inputen.
	int b{inputInteger()}; //Med den andre ville bare inputen blitt printet, og jeg kunne ikke brukt den videre
	cout << "Summen av tallene " << (a+b) << endl;
	return;
}

//1e
bool isOdd(int n){
	if (n%2==1){
		return true;
	}
	return false;
}
// stupid boi, this is the way
bool newIsOdd(int n){return (n%2 == 1);}

//1f
void printHumanReadableTime(unsigned int seconds){
	vector<unsigned int> times{1, 60, 3600, 86400, 31557600, 315576000, 3155760000};
	vector<string> timenames{" seconds ", " minutes ", " hours ", " days ", " years ", " decades ", " centuries "};

	for (int x=times.size()-1; x>=0; x--){//løkken går feil vei siden jeg skrev vektorene i feil rekkefølge. Løkken går størst til minst
		if (seconds/(times[x])!=0){ //hvis inputen er stor nok så skal den tilsvarende tids-størrelsen printes
			cout << seconds/(times[x]) << timenames[x]; //printer antallet timer, dager ect
			seconds -= (seconds/(times[x]))*times[x]; //trekker fra noen sekunder i inputen så det blir riktig i neste runde i løkken
		}
	}
	cout << endl;
	return;
}

//2a
void inputManyIntegersAndPrintSum(){
	cout << "Skriv inn hvor mange tall du vil skrive inn ";
	int n;
	cin >> n;
	int sum=0;
	int temp=0;
	cout << endl;
	for(int x=0; x<n; x++){
		cout << "Skriv inn et tall ";
		cin >> temp;
		sum += temp;
	}
	cout << "Summen er " << sum << endl;
	return;
}

//2b
void inputUntilZero(){
	int n=0;
	int sum=0;
	do{
		cout << "Skriv inn et tall ";
		cin >> n;
		sum += n;
	}
	while (n!=0);
	cout << "Summen er " << sum << endl;
}

//2c
//i den første skal du kjøre kode et bestemt antall ganger, da er for-løkker best.
//i den andre skal du kjøre kode et uvisst antall ganger. da er while lurt.
//i den andre er do-while best, siden da får du alltid minst en input. 

//2d
double inputDouble(){
	cout << "Skriv inn et desimaltall ";
	double n;
	cin >> n;
	return n;
}

//2e
void nokToEur(){
	cout << "Skriv inn hvor mange kroner (NOK) du har " << endl;
	double nok;
	do{
		nok = inputDouble();
		cout << endl;
		if (nok<0){
			cout << "Kan ikke konvertere negative tall" << endl;;
		}
	}
	while (nok<0);
	double eur = nok/9.81;
	cout << fixed << showpoint << setprecision(2);
	cout << nok << " kr er " << eur << " euro" << endl;
	return;
}

//2f 
//Oppgaven ber eksplisitt om et desimaltall som input, derfor kan man ikke bruke inputInteger.
//returtypen jeg valgte er void, siden funksjonen ikke trenger å returnere noe men bare printe til skjermen

//3b
void multiplicationTable(int width, int height){
	//lager en 2D-vektor med gangetabellen
	//hadde ikke trengt å lage den, kunne printet direkte, men mer læring på denne måten
	vector<vector<int>> y (height);
	vector<int> x (width);
	for (int i=1; i<height+1; i++){
		for (int j=1; j<width+1; j++){
			x[j-1] = j*i;
		}
		y[i-1] = x;
	}

	//print ut 2D-vektoren
	for (int i=0; i<static_cast<int>(y.size()); i++){
		for (int j=0; j<static_cast<int>(x.size()); j++){
			cout << setw(5) << y[i][j];
		}
		cout << "\n\n";
	}
	return;
}

//4a
double discriminant(double a, double b, double c){
	return pow(b,2)-4*a*c;
}

//4b
void printRealRoots(double a, double b, double c){
	double discr = discriminant(a, b, c);
	if (discr<0){
		cout << "Ingen reelle røtter" << endl;
	}
	else if (discr>0){
	double solution_1 = (-b+sqrt(discr))/(2*a);
	double solution_2 = (-b-sqrt(discr))/(2*a);
	cout << "Løsning én: x=" << solution_1 << endl;
	cout << "Løsning to: x=" << solution_2 << endl;
	}
	else{
		double solution = -b/(2*a);
		cout << "Løsningen er x=" << solution << endl;
	}
	return;
}

//4c
void solveQuadraticEquations(){
	double a;
	double b;
	double c;
	cout << "Skriv inn koeffisienten a: ";
	cin >> a;
	cout << endl;
	cout << "Skriv inn koeffisienten b: ";
	cin >> b;
	cout << endl;
	cout << "Skriv inn koeffisienten c: ";
	cin >> c;
	cout << endl;
	printRealRoots(a, b, c);
	return;
}

//5
void pythagoras(){
	using namespace Graph_lib;
	Simple_window win{Point{100, 100}, 600, 600, "Pythagoras"};
	
	Polygon triangle;
	triangle.add(Point{200, 200});
	triangle.add(Point{200, 350});
	triangle.add(Point{400, 350});
	triangle.set_fill_color(Color:: red);

	Polygon square_a;
	square_a.add(Point{200, 200});
	square_a.add(Point{200, 350});
	square_a.add(Point{50, 350});
	square_a.add(Point{50, 200});
	square_a.set_fill_color(Color:: blue);

	Polygon square_b;
	square_b.add(Point{200, 350});
	square_b.add(Point{400, 350});
	square_b.add(Point{400, 550});
	square_b.add(Point{200, 550});
	square_b.set_fill_color(Color:: green);

	Polygon square_c;
	square_c.add(Point{200, 200});
	square_c.add(Point{400, 350});
	square_c.add(Point{550, 150});
	square_c.add(Point{350, 0});
	square_c.set_fill_color(Color:: yellow);

	win.attach(triangle);
	win.attach(square_a);
	win.attach(square_b);
	win.attach(square_c);
	win.wait_for_button();
}

//6a
vector<int> calculateSeries(int amount, int intrest, int years){
	int remaining = amount;
	vector<int> payments;
	while (remaining>0){
		payments.push_back((amount/years)+(static_cast<double>(intrest)/100)*remaining);
		remaining -= (amount/years);
	}
	return payments;
}

//6b
vector<int> calculateAnnuity(int amount, int intrest, int years){
	double intrest_percent = intrest/100.0;
	int payment = amount*(intrest_percent/(1-pow(1+intrest_percent, -years)));
	vector<int> payment_list (years, payment);
	return payment_list;
}

//Testfunksjon for å printe individuelle lån. 1=serie, 2=annuitet.
void printLoanList(int type){
	cout << "Skriv inn lånebeløpet: ";
	int loan;
	cin >> loan;
	cout << "\nSkriv inn renten i prosent: ";
	int intrest;
	cin >> intrest;
	cout << "\nSkriv inn anntallet avdrag: ";
	int years;
	cin >> years;
	vector<int> payments{0};
	switch(type){
		case 1:{
			vector<int> payments = calculateSeries(loan, intrest, years);
			break;
		}
		case 2:{
			vector<int> payments = calculateAnnuity(loan, intrest, years);
			break;
		}
		default:{
			break;
		}
	}
	cout << setw(3) << "År" << setw(15) << "Innbetalinger" << endl;
	for(int i=0; i<years; i++){
		cout << setw(3) << i+1 << setw(15) << payments[i] << endl;
	}
	return;
}

//6c
void printBothLoans(int amount, int intrest, int years){
	vector<int> series = calculateSeries(amount, intrest, years);
	int series_sum = 0;
	for(int x=0; x<years; x++){
		series_sum += series[x];
	}

	vector<int> annuity = calculateAnnuity(amount, intrest, years);
	int annuity_sum = 0;
	for(int x=0; x<years; x++){
		annuity_sum += annuity[x];
	}

	cout << setw(5) << "År" << setw(10) << "Serie" << setw(15) << "Annuitet" << setw(15) << "Differanse" << endl;
	for(int i=0; i<years; i++){		
		cout << setw(5) << i+1 << setw(10) << series[i] << setw(15) << annuity[i] << setw(15) << series[i]-annuity[i] << endl;
	}
	cout << setw(5) << "Total" << setw(10) << series_sum << setw(15) << annuity_sum << setw(15) << series_sum-annuity_sum << endl;
	return;
}

int main(){
	cout << "Velg funksjon\n" << "0  Avslutt\n" << "1  Summere to tall\n" << "2  Summere flere tall\n";
	cout << "3  Konvertere NOK til Euro\n" << "4  Gangetabell\n" << "5  Andregradslikninger\n";
	cout << "6  Tegne en rettvinklet trekant\n" << "7  Beregne avdrag på serielån\n" << "8  Beregne avdrag på annuitetslån\n";
	cout << "9  Differanse mellom serie- og annuitetslån\n" << "10 Test oppgave 1 og 2\n";
	int choice;
	//bruker en do-while så man kan gjøre så mye man vil. Kjører så lenge input!=0
	do{
	cout << "Angi valg (0-10): ";
	cin >> choice;
	switch (choice){
		case 1:
			inputIntegersAndPrintSum();
			break;
		case 2:
			inputManyIntegersAndPrintSum();
			break;
		case 3:
			nokToEur();
			break;
		case 4:{
			cout << "Angi bredden: ";
			int width;
			cin >> width;
			cout << "\nAngi hoyden: ";
			int height;
			cin >> height;
			multiplicationTable(width, height);
			break;
		}
		case 5:
			solveQuadraticEquations();
			break;
		case 6:
			pythagoras();
			break;
		case 7:{
			printLoanList(1);
			break;
		}
		case 8:{
			printLoanList(2);
			break;
		}
		case 9:{
			cout << "Skriv inn lånebeløpet: ";
			int loan;
			cin >> loan;
			cout << "\nSkriv inn renten i prosent: ";
			int intrest;
			cin >> intrest;
			cout << "\nSkriv inn anntallet avdrag: ";
			int years;
			cin >> years;
			printBothLoans(loan, intrest, years);
			break;
		}
		case 10:{
			//Oppgave 1
			cout << "inputAndPrintInteger" << endl;
			inputAndPrintInteger();

			cout << "\ninputInteger" << endl;
			int number = inputInteger();
			cout << "Du skrev: " << number << endl;

			cout <<"\nisOdd på [0,15]" << endl;
			for (int x=0; x<=15; x++){
				cout << x << " " << isOdd(x) << endl;
			}
			
			cout << "\nprintHumanReadableTime(10 000)" << endl;
			printHumanReadableTime(10000);

			cout << "\nprintHumanReadableTime(1 000 000 000)" << endl;
			printHumanReadableTime(1000000000);

			//Oppgave 2
			cout << "\ninputManyIntegersAndPrintSum" << endl;
			inputManyIntegersAndPrintSum();

			cout << "\ninputUntilZero" << endl;
			inputUntilZero();

			cout << "\ninputDouble" << endl;
			double decimal = inputDouble();
			cout << "Du skrev inn " << decimal << endl;
			break;
		}
		default:
			break;
		}
	}
	while (choice != 0);

	return 0;
}