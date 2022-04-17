#include "physics.h"
#include "utils.h"

#include <stdio.h>
#include <math.h>

// precalculate constants
static double aL = 0;
static int precalc_finished = 0;
static precalc(){
    if (!precalc_finished){
        aL = constants->ALPHA * constants->L;
    }
}

int f_t(double t){
    if (constants->TAU == 0.0) return 0;
    return (3.0/4.0*constants->TAU <= fmod(t, constants->TAU));
}

double U_r(double x){
    precalc();
    x = fmod(x, constants->L);
    if (is_in_range(x, 0, aL)){
        return x / aL;
    }
    else if (is_in_range(x, aL, constants->L)){
        return (constants->L - x) / (constants->L - aL);
    }
    // sanity check
    else return 0.0;
}

static double F_r(double x){
    // -nabla U
    precalc();
    x = fmod(x, constants->L);
    if (is_in_range(x, 0, aL)){
        return -constants->L / constants->ALPHA;
    }
    else if (is_in_range(x, aL, constants->L)){
        return constants->L / (constants->L - aL);
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
