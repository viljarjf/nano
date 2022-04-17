#include "euler.h"

#include <math.h>

void euler_scheme(double *x_hat, double *t, reduced_constants_t *red_consts){
    double dU = -F_reduced(*x_hat, *t);
    *x_hat += - dU * red_consts->DELTA_T_HAT + sqrt(2 * red_consts->D * red_consts->DELTA_T_HAT) * rng();
    *t += constants->DELTA_T;
}
