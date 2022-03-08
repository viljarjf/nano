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
    numpy_file_t *datafile = malloc(sizeof(numpy_file_t));
    numpy_file_t *timefile = malloc(sizeof(numpy_file_t));
    get_numpy_file("particles", shape, 2, FLOAT64, datafile);
    get_numpy_file("time", shape, 2, FLOAT64, timefile);


    for (int p = 0; p < N_PARTICLES; p++){
        xi = x0;
        ti = t0;
        for (int i = 0; i < N_STEPS; i++){
            euler_scheme(&xi, &ti, R1);
            write_to_numpy_file(datafile, &xi, FLOAT64);          
            write_to_numpy_file(timefile, &ti, FLOAT64);          
        }
    }
    close_numpy_file(datafile);
    close_numpy_file(timefile);

    return 0;
}
