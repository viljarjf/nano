#include <stdio.h>
#include <stdlib.h>

#include "euler.h"

#define N_PARTICLES 100
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
        for (int i = 0; i < N_STEPS; i++){
            euler_scheme(&xi, &ti, R1);
            fprintf(fptr, "%f\n", xi);
        }
        fprintf(fptr, ";\n");
    }

    fclose(fptr);

    return 0;
}
