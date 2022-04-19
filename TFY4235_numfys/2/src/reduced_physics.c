#include "reduced_physics.h"
#include "utils.h"
#include "constants.h"

#include <stdio.h>
#include <math.h>

double U_r_reduced(double x_hat){
    x_hat = fmod(fmod(x_hat, 1) + 1, 1);
    if (is_in_range(x_hat, 0, constants->ALPHA)){
        return x_hat / constants->ALPHA;
    }
    else if (is_in_range(x_hat, constants->ALPHA, 1)){
        return (1 - x_hat) / (1 - constants->ALPHA);
    }
    // sanity check
    else return 0.0;
}

double F_r_reduced(double x_hat){
    x_hat = fmod(fmod(x_hat, 1) + 1, 1);
    if (is_in_range(x_hat, 0, constants->ALPHA)){
        return -1 / constants->ALPHA;
    }
    else if (is_in_range(x_hat, constants->ALPHA, 1)){
        return 1 / (1 - constants->ALPHA);
    }
    // sanity check
    else return 0.0;
}

double U_reduced(double x_hat, double t){
    return U_r_reduced(x_hat) * f_t(t);
}

double F_reduced(double x_hat, double t){
    return F_r_reduced(x_hat) * f_t(t);
}

double calc_delta_t_hat(reduced_constants_t *reduced_constants){
    double D = reduced_constants->D;
    double a = constants->ALPHA;
    double F = fmax(fabs(F_r_reduced(0)), fabs(F_r_reduced(a)));
    return (
        4*sqrt(2)*sqrt(a*D*F + 8*D*D) + 
        a*F + 16*D
        ) / (F*F);
}

double reduced_bolzmann_distribution(double x_hat){
    double norm = constants->DELTA_U / constants->KBT;
    return norm * exp(-U_r_reduced(x_hat)*norm) / (1 - exp(-norm));
}
