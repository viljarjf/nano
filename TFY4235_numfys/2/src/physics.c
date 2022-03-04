#include "physics.h"
#include <math.h>

static int f_t(double t){
    return (3/4*TAU <= fmod(t, TAU) && fmod(t, TAU) < TAU);
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

    if (0 <= x && x < ALPHA){
        return -1 / ALPHA;
    }
    else if (ALPHA <= x && x < 1){
        return 1 / (1 - ALPHA);
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
