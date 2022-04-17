#include <stdio.h>
#include <stdlib.h>

#include "euler.h"
#include "numpy_IO.h"
#include "rng.h"

#define N_PARTICLES 100
#define N_STEPS     100000

// initialize constants
constants_t tmp = {
    .L         =  20e-6,                // [m]
    .ALPHA     =  0.1,                  // [~]
    .TAU       =  1.0,                    // [s]
    .DELTA_U   =  80*ELECTRONVOLT,      // [J]
    .KBT       =  0.0026*ELECTRONVOLT,  // [J]
    .R1        =  12e-9,                // [m]
    .DELTA_T   =  0.01                // [s]  IDK man, har ikke regna på det enda
};
constants_t *constants = &tmp;

int main(int argsc, char *argv[]){
    // based
    
    char header[31] = "##############################";
    printf("%s\n#   Biased Brownian Motion   #\n%s\n", header, header);

    srand((unsigned)time());
    
    double calc_dt = calc_delta_t();
    printf("Upper bound delta t: %f\n", calc_dt);
    printf("Current delta t: %f\n", constants->DELTA_T);
    if(constants->DELTA_T / calc_dt > 2){
        printf("Setting delta t to half of upper bound\n");
        constants->DELTA_T = calc_dt / 2;
        printf("New delta t: %f\n", constants->DELTA_T);
    }

    int shape[2] = {N_PARTICLES, N_STEPS};
    int flat_shape[2] = {N_STEPS, 2};
    numpy_file_t *data = malloc(sizeof(numpy_file_t));
    numpy_file_t *timef = malloc(sizeof(numpy_file_t));
    numpy_file_t *potential = malloc(sizeof(numpy_file_t));
    numpy_file_t *bolzmann = malloc(sizeof(numpy_file_t));
    make_numpy_file("particles", shape, 2, FLOAT64, data);
    make_numpy_file("time", shape, 2, FLOAT64, timef);
    make_numpy_file("potential", flat_shape, 2, FLOAT64, potential);
    make_numpy_file("bolzmann", flat_shape, 2, FLOAT64, bolzmann);


    double x0 = 0.3;
    double t0 = 0;

    double xi_hat;
    double ti;

    double write_buffer = 0;

    reduced_constants_t *reduced_constants = malloc(sizeof(reduced_constants_t));
    get_reduced_constants(reduced_constants, constants);

    printf("D: %f\n", reduced_constants->D);
    double calc_dt_hat = calc_delta_t_hat(reduced_constants);
    printf("Upper bound delta t hat: %f\n", calc_dt_hat);
    printf("Current delta t hat: %f\n", reduced_constants->DELTA_T_HAT);
    if(reduced_constants->DELTA_T_HAT / calc_dt_hat > 2){
        printf("Setting delta t to half of upper bound\n");
        reduced_constants->DELTA_T_HAT = calc_dt_hat / 2;
        printf("New delta t: %f\n", reduced_constants->DELTA_T_HAT);
    }

    for (int p = 0; p < N_PARTICLES; p++){
        ti = t0;
        xi_hat = uniform();
        for (double i = 0; i < N_STEPS; i++){
            euler_scheme(&xi_hat, &ti, reduced_constants);

            write_to_numpy_file(data, &xi_hat, FLOAT64);
            write_to_numpy_file(timef, &ti, FLOAT64);

            // only do potential-stuff once
            if(!p){
                write_buffer = f_t(ti);
                write_to_numpy_file(potential, &write_buffer, FLOAT64);

                // hack to get regularly spaced data
                write_buffer = U_r_reduced(ti);
                write_to_numpy_file(potential, &write_buffer, FLOAT64);

                write_buffer = reduced_bolzmann_distribution(i / (double)N_STEPS);
                write_to_numpy_file(bolzmann, &write_buffer, FLOAT64);
                write_buffer = i / (double)N_STEPS;
                write_to_numpy_file(bolzmann, &write_buffer, FLOAT64);
            }
        }
    }
    close_numpy_files();
    return 0;
}
