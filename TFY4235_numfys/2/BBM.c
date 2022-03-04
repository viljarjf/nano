#include <stdio.h>
#include <stdlib.h>

#include "euler.h"

#define N_PARTICLES 1000
#define N_STEPS     10000

int main(int argsc, char *argv[]){
    // based
    printf("Biased Brownian Motion\n");
    srand((unsigned) time());

    printf("Upper bound delta t: %f\n", calc_delta_t(R1));
    
    double x0 = 0;
    double t0 = 0;

    double xi;
    double ti;

    FILE *fptr = fopen("data/particles.txt", "w");

    for (int p = 0; p < N_PARTICLES; p++){
        xi = x0;
        ti = t0;
        for (int i = 0; i < N_STEPS; i++){
            xi = euler_scheme(xi, &ti, R1);
        }
        fprintf(fptr, "%f\n", xi);
    }

    fclose(fptr);

    return 0;
}
