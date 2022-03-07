#include "physics.h"

#include <stdio.h>
#include <math.h>

static int f_t(double t){
    if (TAU == 0.0) return 0;
    int v = (3.0/4.0*TAU <= fmod(t, TAU));
    //printf("%i %f %f\n", v, fmod(t, TAU), 3.0/4.0*TAU);
    return v;
}

static double U_r(double x){
    if (0 <= fmod(x, 1) && fmod(x, 1) < ALPHA){
        return x / ALPHA;
    }
    else if (ALPHA <= fmod(x, 1) && fmod(x, 1) < 1){
        return (1 - x) / (1 - ALPHA);
    }
    // sanity check
    else return 0.0;
}

static double F_r(double x){
    // -nabla U

    if (0 <= fmod(x, 1) && fmod(x, 1) < ALPHA){
        return -1.0 / ALPHA;
    }
    else if (ALPHA <= fmod(x, 1) && fmod(x, 1) < 1){
        return 1.0 / (1 - ALPHA);
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
