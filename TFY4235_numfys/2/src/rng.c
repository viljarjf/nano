#include "rng.h"
#include "stdlib.h"
#include "math.h"

#define PI 3.14159

/**
 * @brief Return a pseudo-random number, uniformly distibuted in [0, 1]
 * 
 * @return double 
 */
static double uniform(){
    return rand() / (double)RAND_MAX;
}

double rng(){
    // https://en.wikipedia.org/wiki/Box%E2%80%93Muller_transform
    double u1 = uniform();
    double u2 = uniform();
    return sqrt(-2*log(u1)) * cos(2*PI*u2);
    // return sqrt(-2*log(u1)) * sin(2*PI*u2);  // Independent, same distribution
}
