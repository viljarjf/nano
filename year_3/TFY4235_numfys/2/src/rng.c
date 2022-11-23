#include "rng.h"
#include "constants.h"

#include <stdlib.h>
#include <math.h>
#include <stdio.h>



/**
 * @brief Return a pseudo-random number, uniformly distibuted in [0, 1]
 * 
 * @return double 
 */
double uniform(){
    return rand() / (double)RAND_MAX;
}

double rng(){
    // https://en.wikipedia.org/wiki/Box%E2%80%93Muller_transform
    double u1 = uniform();
    double u2 = uniform();
    return sqrt(-2*log(u1)) * cos(2*PI*u2);
    // return sqrt(-2*log(u1)) * sin(2*PI*u2);  // Independent, same distribution
}

void write_to_file(int n){
    // write a bunch of random numbers to file for easy plotting in python
    // to verify the distribution
    FILE *fptr = fopen("randnums.txt", "w");

    for (int i = 0; i < 10000; i++){
        fprintf(fptr, "%f\n", rng());
    }
    fclose(fptr);
}
