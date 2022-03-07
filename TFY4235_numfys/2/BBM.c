#include <stdio.h>
#include <stdlib.h>

#include "euler.h"
#include "utils.h"

#define N_PARTICLES 100
#define N_STEPS     100000

int main(int argsc, char *argv[]){
    // based
    printf("Biased Brownian Motion\n");
    srand((unsigned)time());

    printf("Upper bound delta t: %f\n", calc_delta_t(R1));
    
    double x0 = 0;
    double t0 = 0;

    double xi = x0;
    double ti = t0;

    int shape[2] = {N_PARTICLES, N_STEPS};
    FILE *fptr = get_numpy_file("data/particles.npy", shape, 2, FLOAT64);

    for (int p = 0; p < N_PARTICLES; p++){
        for (int i = 0; i < N_STEPS; i++){
            euler_scheme(&xi, &ti, R1);
            
            fwrite(&xi, sizeof(xi), 1, fptr);
        }
    }

    fclose(fptr);

    return 0;
}
