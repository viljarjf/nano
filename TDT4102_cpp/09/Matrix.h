#pragma once
#include <iostream>

class Matrix{
    int rows;
    int columns;
    double** table;

    public:
        Matrix();
        Matrix(int nRows, int nColumns);
        explicit Matrix(int nRows);
        ~Matrix();
        Matrix(const Matrix & rhs);

        double get(int row, int col) const;
        void set(int row, int col, double value);
        int getRows() const;
        int getColumns() const;
        bool isValid() const;

        double* operator[](int& row) const;
        Matrix& operator=(Matrix);
        Matrix& operator+=(Matrix);
        Matrix& operator+(Matrix);
};

std::ostream& operator<<(std::ostream&, Matrix&);

void testMatrix();
