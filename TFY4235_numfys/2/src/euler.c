#include "euler.h"

#include <math.h>

void euler_scheme(double *x, double *t, double r){
    double omega = 1 / (6*PI*ETA*r*constants->L*constants->L);
    double D = constants->KBT;
    double dU = F(*x*constants->L, *t);
    *x += - dU * constants->DELTA_T * omega + sqrt(2 * D * constants->DELTA_T * omega) * rng();
    *t += constants->DELTA_T;
}

double calc_delta_t(double r){
    double max_F = constants->ALPHA < 0.5 ? 1/constants->ALPHA : 1/(1-constants->ALPHA);
    double gamma = 6*PI*ETA*r;
    double kBT = 32*constants->KBT;
    return (
        sqrt(kBT) * gamma * sqrt(4 * constants->ALPHA * constants->L + kBT) + 
        2 * constants->ALPHA * constants->L * gamma * max_F + kBT * gamma
        ) / (2 * max_F * max_F);
}
