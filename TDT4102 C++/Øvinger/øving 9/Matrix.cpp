#include "Matrix.h"
#include <iostream>
#include <iomanip>
#include <utility>


//Constructors
Matrix::Matrix(): rows{0}, columns{0}, table{nullptr} {}

Matrix::Matrix(int nRows, int nColumns) : rows{nRows}, columns{nColumns} {
    table = new double*[rows];
     for (int row=0; row<rows; row++){
        table[row] = new double[columns];
        for(int col=0; col<columns; col++){
            table[row][col]=0;
        }
    }
}

Matrix::Matrix(int nRows) : Matrix(nRows, nRows) {
    for(int n=0; n<rows; n++){
        table[n][n]=1;
    }
}

Matrix::~Matrix(){
    for (int n=0; n<rows; n++){
        delete[] table[n];          
    }
    delete[] table;
}

Matrix::Matrix(const Matrix & rhs){
    rows = rhs.rows;
    columns = rhs.columns;
    if (rhs.isValid()){
        table = new double*[rows];

        for(int row=0; row<rows; row++){
            table[row] = new double[columns];
            for(int col=0; col<columns; col++){
                table[row][col] = rhs.get(row, col);
            }
        }
    }
    else{
        table=nullptr;
    }
}


//Member functions
double Matrix::get(int row, int col) const{
    return table[row][col];
}

void Matrix::set(int row, int col, double value){
    table[row][col]=value;
}

int Matrix::getRows() const{
    return rows;
}

int Matrix::getColumns() const{
    return columns;
}

bool Matrix::isValid() const{
    return (table != nullptr);
}


//Operators
double* Matrix::operator[](int& row) const{
    if (this->isValid()){
        return table[row];
    }
    std::cout << "Matrix is invalid. Returning 0.\n";
    return 0;
}

std::ostream& operator<<(std::ostream& os, Matrix& m){
    if (!m.isValid()){
        os << "Invalid matrix\n";
        return os;
    }

    for(int row=0; row<m.getRows(); row++){
        for(int col=0; col<m.getColumns(); col++){
            os << std::setw(5) << m[row][col] << " ";
        }
        os << "\n\n";
    }
    return os;
}

Matrix& Matrix::operator=(Matrix rhs){
    std::swap(rows, rhs.rows);
    std::swap(columns, rhs.columns);
    std::swap(table, rhs.table);

    return *this;
}

Matrix& Matrix::operator+=(Matrix rhs){
    if (rows != rhs.rows || columns != rhs.columns){
        rows=0;
        columns=0;
        table=nullptr;
    }
    else{
        for(int row=0; row<rhs.rows; row++){
            for(int col=0; col<rhs.columns; col++){
                table[row][col]+=rhs[row][col];
            }
        }
    }
    return *this;
}

Matrix& Matrix::operator+(Matrix rhs){
    *this+=rhs;
    return *this;
}


//test function
void testMatrix(){
    using namespace std;

    cout << "Invalid matrix: \n";
    Matrix invalid{};
    cout << invalid;
    cout << "\nZero-matrix a (5x3): \n";
    Matrix a{5, 3};
    cout << a;
    cout << "\nIdentity matrix b (7x7):\n";
    Matrix b{7};
    cout << b;
    cout << "\nCopy the previous matrix into a new one:\n";
    Matrix b_copy{b};
    cout << b_copy;
    cout << "\nAdd n to the diagonal of b with set():\n";
    for(int n=0; n<b.getRows(); n++){
        b.set(n, n, b.get(n, n)+n);
    }
    cout << b;
    cout << "\nCheck the copy of b:\n";
    cout << b_copy;
    cout << "\nb_copy += a. Printing b_copy yields: \n";
    b_copy+=a;
    cout << b_copy;
    cout << "\n a = b. Printing a yields: \n";
    a=b;
    cout << a;
    cout << "\nb += a. Printing b yields: \n";
    b+=a;
    cout << b;
    cout << "\nc = a+b. Printing c yields: \n";
    Matrix c;
    c=a+b;
    cout << c;
    
    cout << "\n\nA, B, and C as given in the task:\n";
    Matrix A{2, 2};
    A.set(0,0,1);
    A.set(0,1,2);
    A.set(1,0,3);
    A.set(1,1,4);
    cout << "A:\n" << A;

    Matrix B{2, 2};
    B.set(0,0,4);
    B.set(0,1,3);
    B.set(1,0,2);
    B.set(1,1,1);
    cout << "B:\n" << B;

    Matrix C{2, 2,};
    C.set(0,0,1);
    C.set(0,1,3);
    C.set(1,0,1.5);
    C.set(1,1,2);
    cout << "C:\n" << C;

    cout << "A += B+C. Printing A yields:\n";
    A += B+C;
    cout << A;
}