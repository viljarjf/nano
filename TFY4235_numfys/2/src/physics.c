#include "physics.h"
#include "utils.h"

#include <stdio.h>
#include <math.h>


int f_t(double t){
    if (constants->TAU == 0.0) return 0;
    return (3.0/4.0*constants->TAU <= fmod(t, constants->TAU));
}

double U_r(double x){
    if (is_in_mod_range(x, 0, constants->ALPHA * constants->L, constants->L)){
        return x / (constants->ALPHA * constants->L);
    }
    else if (is_in_mod_range(x, constants->ALPHA * constants->L, constants->L, constants->L)){
        return (constants->L - x) / (constants->L * (1 - constants->ALPHA));
    }
    // sanity check
    else return 0.0;
}

static double F_r(double x){
    // -nabla U
    x = fabs(x);
    if (0 <= fmod(x, 1) && fmod(x, 1) < constants->ALPHA){
        return -1.0 / constants->ALPHA;
    }
    else if (constants->ALPHA <= fmod(x, 1) && fmod(x, 1) < 1){
        return 1.0 / (1 - constants->ALPHA);
    }
    // sanity check
    else return 0.0;
}

double U(double x, double t){
    return U_r(x) * f_t(t);
}

double F(double x, double t){
    return F_r(x) * f_t(t);
}
