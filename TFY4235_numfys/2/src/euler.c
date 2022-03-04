#include "euler.h"

#include <math.h>

double euler_scheme(double x, double t, double r){
    double gamma_inv = 1 / (6*PI*ETA*r);
    return x - gamma_inv * F(x, t) * DELTA_T + sqrt(2 * KBT * DELTA_T * gamma_inv) * rng();
}

double calc_delta_t(double r){
    double max_F = ALPHA < 0.5 ? 1/ALPHA : 1/(1-ALPHA);
    double gamma = 6*PI*ETA*r;
    double kBT = 32*KBT;
    return (sqrt(kBT) * gamma * sqrt(4 * ALPHA * L + kBT) + 2 * ALPHA * L * gamma * max_F + kBT * gamma) / (2 * max_F * max_F);
}
