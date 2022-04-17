#include <stdio.h>
#include <stdlib.h>

#include "euler.h"
#include "utils.h"

#define N_PARTICLES 100
#define N_STEPS     100000

// initialize constants
constants_t tmp = {
    .L         =  1,            // [nm]
    .ALPHA     =  0.95,          // [~]
    .TAU       =  0.1,           // [s]
    .DELTA_U   =  80.0,         // [eV]
    .KBT       =  0.026,        // [eV]
    .R1        =  12.0,         // [nm]
    .DELTA_T   =  0.001         // [s]  IDK man, har ikke regna på det enda
};
const constants_t *constants = &tmp;

int main(int argsc, char *argv[]){
    // based
    printf("Biased Brownian Motion\n");
    srand((unsigned)time());

    printf("Upper bound delta t: %f\n", calc_delta_t(constants->R1));
    
    double x0 = 0;
    double t0 = 0;

    double xi = x0;
    double ti = t0;

    int shape[2] = {N_PARTICLES, N_STEPS};
    int flat_shape[2] = {N_STEPS, 2};
    numpy_file_t *data = malloc(sizeof(numpy_file_t));
    numpy_file_t *timef = malloc(sizeof(numpy_file_t));
    numpy_file_t *potential = malloc(sizeof(numpy_file_t));
    make_numpy_file("particles", shape, 2, FLOAT64, data);
    make_numpy_file("time", shape, 2, FLOAT64, timef);
    make_numpy_file("potential", flat_shape, 2, FLOAT64, potential);


    double pot = 0;
    for (int p = 0; p < N_PARTICLES; p++){
        xi = x0;
        ti = t0;
        for (int i = 0; i < N_STEPS; i++){
            euler_scheme(&xi, &ti, constants->R1);
            write_to_numpy_file(data, &xi, FLOAT64);          
            write_to_numpy_file(timef, &ti, FLOAT64);
            if(!p){
                pot = f_t(ti);
                write_to_numpy_file(potential, &pot, FLOAT64);
                pot = U_r(ti);
                write_to_numpy_file(potential, &pot, FLOAT64);
            }
        }
    }
    close_numpy_files();
    return 0;
}
