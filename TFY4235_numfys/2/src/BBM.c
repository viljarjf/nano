#include <stdio.h>
#include <stdlib.h>

#include "euler.h"
#include "numpy_IO.h"
#include "rng.h"

#define N_PARTICLES 100000
#define N_STEPS     5000


// initialize constants
constants_t tmp = {
    .L         =  20e-6,                // [m]
    .ALPHA     =  0.1,                 // [~]
    .TAU       =  2,                 // [s]
    .DELTA_U   =  80*ELECTRONVOLT,      // [J]
    .KBT       =  0.0026*ELECTRONVOLT,  // [J]
    .R1        =  12e-9,                // [m]
    .DELTA_T   =  0.00005                  // [s]  IDK man, har ikke regna på det enda
};
constants_t *constants = &tmp;


typedef struct {
    numpy_file_t *data;
    numpy_file_t *timef;
    numpy_file_t *potential;
    numpy_file_t *bolzmann;
    numpy_file_t *tau;
    reduced_constants_t *reduced_constants;
} runtime_struct_t;


void setup(runtime_struct_t *s){
    double calc_dt = calc_delta_t();
    printf("  Upper bound delta t: %f\n", calc_dt);
    printf("  Current delta t: %f\n", constants->DELTA_T);
    /*
    if(constants->DELTA_T / calc_dt > 2){
        printf(" Setting delta t to half of upper bound\n");
        constants->DELTA_T = calc_dt / 2;
        printf(" New delta t: %f\n", constants->DELTA_T);
    }
    */

    int full_shape[2] = {N_PARTICLES, N_STEPS};
    int steps_shape_2d[2] = {N_STEPS, 2};
    int steps_shape_1d[2] = {N_STEPS, 1};
    int particles_shape_1d[2] = {N_PARTICLES, 1};
    s->data = malloc(sizeof(numpy_file_t));
    s->timef = malloc(sizeof(numpy_file_t));
    s->potential = malloc(sizeof(numpy_file_t));
    s->bolzmann = malloc(sizeof(numpy_file_t));
    s->tau = malloc(sizeof(numpy_file_t));
    make_numpy_file("particles", full_shape, 2, FLOAT32, s->data);
    make_numpy_file("time", steps_shape_1d, 2, FLOAT64, s->timef);
    make_numpy_file("potential", steps_shape_2d, 2, FLOAT64, s->potential);
    make_numpy_file("bolzmann", steps_shape_2d, 2, FLOAT64, s->bolzmann);
    make_numpy_file("tau", particles_shape_1d, 2, FLOAT64, s->tau);

    s->reduced_constants = malloc(sizeof(reduced_constants_t));
    get_reduced_constants(s->reduced_constants, constants);

    printf("  D: %f\n", s->reduced_constants->D);
    double calc_dt_hat = calc_delta_t_hat(s->reduced_constants);
    printf("  Upper bound delta t hat: %f\n", calc_dt_hat);
    printf("  Current delta t hat: %f\n", constants->TAU);
    /*
    if(reduced_constants->DELTA_T_HAT / calc_dt_hat > 2){
        printf(" Setting delta t to half of upper bound\n");
        reduced_constants->DELTA_T_HAT = calc_dt_hat / 2;
        printf(" New delta t: %f\n", reduced_constants->DELTA_T_HAT);
    }
    */

}


void run(runtime_struct_t *s){
    
    double xi_hat;
    double ti;

    double write_buffer = 0;
    float xi_hat_float = 0;

    for (int p = 0; p < N_PARTICLES; p++){

        // initial state of system
        ti = 0;
        xi_hat = uniform();
        

        for (double i = 0; i < N_STEPS; i++){
            euler_scheme(&xi_hat, &ti, s->reduced_constants);

            xi_hat_float = (float)xi_hat;
            write_to_numpy_file(s->data, &xi_hat_float, FLOAT32);

            // only do potential-stuff once
            if(!p){
                write_to_numpy_file(s->timef, &ti, FLOAT64);
                write_buffer = f_t(ti);
                write_to_numpy_file(s->potential, &write_buffer, FLOAT64);

                // hack to get regularly spaced data
                write_buffer = U_r_reduced(i / (double)N_STEPS);
                write_to_numpy_file(s->potential, &write_buffer, FLOAT64);
                write_buffer = reduced_bolzmann_distribution(i / (double)N_STEPS);
                write_to_numpy_file(s->bolzmann, &write_buffer, FLOAT64);
                write_buffer = i / (double)N_STEPS;
                write_to_numpy_file(s->bolzmann, &write_buffer, FLOAT64);
            }
        }
    }
}


void sweep_tau(runtime_struct_t *s, int n, double start, double end){
    
    double xi_hat;
    double ti;
    float xi_hat_float;

    // do this amount of steps before saving the
    int save_period = 1000;

    // the denominator uses integer division. Should be fine
    double step = (end - start) / (N_PARTICLES / n);

    constants->TAU = start;

    for (int p = 0; p < N_PARTICLES; p++){

        // initial state of system
        ti = 0;
        xi_hat = 0; 

        // change tau every n particles
        if (!(p%n)){
            constants->TAU += step;
        }
        write_to_numpy_file(s->tau, &constants->TAU, FLOAT64);

        for (double i = 0; i < N_STEPS; i++){

            for (int j = 0; j < save_period; j++){
                euler_scheme(&xi_hat, &ti, s->reduced_constants);
            }
            
            xi_hat_float = (float)xi_hat;
            write_to_numpy_file(s->data, &xi_hat_float, FLOAT32);

            if(!p){
                write_to_numpy_file(s->timef, &ti, FLOAT64);
            }
        }
    }
}


int main(int argsc, char *argv[]){
    
    char header[33] = "################################";
    printf("%s\n#    Biased Brownian Motion    #\n%s\n", header, header); // b(i)ased

    srand((unsigned)time());
    
    printf("Starting setup...\n");
    runtime_struct_t *t = malloc(sizeof(runtime_struct_t));
    setup(t);
    printf("Setup complete.\n");

    printf("Starting computation...\n");
    //run(t);
    sweep_tau(t, 1000, 1.0, 3.0);
    printf("Computation complete.\n");

    write_json_metadata(N_PARTICLES, N_STEPS, argv[1]);
    close_numpy_files();

    printf("%s\n#   Data generation complete   #\n%s\n", header, header);

    return 0;
}
