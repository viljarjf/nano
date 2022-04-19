#include "physics.h"
#include "utils.h"

#include <stdio.h>
#include <math.h>

// precalculate constants
static double aL = 0;
static int precalc_finished = 0;
static void precalc(){
    if (!precalc_finished){
        aL = constants->ALPHA * constants->L;
    }
}

int f_t(double t){
    if (constants->TAU == 0.0) return 1;
    return (3.0/4.0*constants->TAU <= fmod(t, constants->TAU));
}

double U_r(double x){
    precalc();
    x = fmod(fmod(x, constants->L) + constants->L, constants->L);
    if (is_in_range(x, 0, aL)){
        return constants->DELTA_U * x / aL;
    }
    else if (is_in_range(x, aL, constants->L)){
        return constants->DELTA_U * (constants->L - x) / (constants->L - aL);
    }
    // sanity check
    else return 0.0;
}

static double F_r(double x){
    // -nabla U
    precalc();
    x = fmod(fmod(x, constants->L) + constants->L, constants->L);
    if (is_in_range(x, 0, aL)){
        return -constants->DELTA_U / aL;
    }
    else if (is_in_range(x, aL, constants->L)){
        return constants->DELTA_U / (constants->L - aL);
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

double calc_delta_t(){
    precalc();
    double max_F = fmax(fabs(F_r(0)), fabs(F_r(aL)));
    double gamma = 6*PI*ETA*constants->R1;
    double kBT = constants->KBT;
    return (
        4*sqrt(2)*sqrt(kBT*gamma*gamma*(8*kBT + aL*max_F)) + 
        gamma * (16 * kBT + aL * max_F)
        ) / (max_F * max_F);
}

double bolzmann_distribution_potential(double U){
    return constants->DELTA_U * exp(- U / constants->KBT) / (constants->KBT * (1 - exp(-constants->DELTA_U / constants->KBT)));
}

double bolzmann_distribution_position(double x){
    return bolzmann_distribution_potential(U_r(x));
}
