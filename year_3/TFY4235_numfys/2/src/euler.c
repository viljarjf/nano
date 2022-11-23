#include "euler.h"

#include <math.h>

void euler_scheme(double *x_hat, double *t){
    double dU = -F_reduced(*x_hat, *t);
    *x_hat += - dU * reduced_constants->DELTA_T_HAT + sqrt(2 * reduced_constants->D * reduced_constants->DELTA_T_HAT) * rng();
    *t += constants->DELTA_T;
}
