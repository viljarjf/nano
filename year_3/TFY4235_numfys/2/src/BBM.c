#include <stdio.h>
#include <stdlib.h>

#include "BBM.h"
#include "rng.h"

#define N_PARTICLES 1000
#define N_STEPS     100

// initialize constants
constants_t tmp = {
    .L         =  20e-6,                // [m]
    .ALPHA     =  0.2,                  // [~]
    .TAU       =  3,                    // [s]
    .DELTA_U   =  80*ELECTRONVOLT,      // [J]
    .KBT       =  0.0026*ELECTRONVOLT,  // [J]
    .R1        =  3*12e-9,              // [m]
    .DELTA_T   =  0.0002                // [s]  IDK man, har ikke regna på det enda
};
constants_t *constants = &tmp;
reduced_constants_t tmp2 = {0,0};
reduced_constants_t *reduced_constants = &tmp2;


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

    update_reduced_constants();

    printf("  D: %f\n", reduced_constants->D);
    double calc_dt_hat = calc_delta_t_hat();
    printf("  Upper bound delta t hat: %f\n", calc_dt_hat);
    printf("  Current delta t hat: %f\n", reduced_constants->DELTA_T_HAT);
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
        xi_hat = 0;//uniform();
        

        for (double i = 0; i < N_STEPS; i++){
            euler_scheme(&xi_hat, &ti);

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
                //write_buffer = reduced_bolzmann_distribution(i / (double)N_STEPS);
                write_buffer = reduced_normal_distribution(-0.5 + i / (double)N_STEPS, constants->DELTA_T*N_STEPS);

                write_to_numpy_file(s->bolzmann, &write_buffer, FLOAT64);
                write_buffer = -0.5 + i / (double)N_STEPS;
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
    // edit two weeks later: it was not
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

        write_to_numpy_file(s->tau, &(constants->TAU), FLOAT64);

        for (double i = 0; i < N_STEPS; i++){

            for (int j = 0; j < save_period; j++){
                euler_scheme(&xi_hat, &ti);
            }
            
            xi_hat_float = (float)xi_hat;
            write_to_numpy_file(s->data, &xi_hat_float, FLOAT32);

            if(!p){
                write_to_numpy_file(s->timef, &ti, FLOAT64);
            }
        }
        printf("\r%u%%", 100*p/N_PARTICLES);
        fflush(stdout);
    }
    printf("\n");
}


void multithread_run(runtime_struct_t *s){
    thread_t *threads[N_PARTICLES];
    for (int i = 0; i < N_PARTICLES; i++){
        threads[i] = open_thread(i, N_STEPS);
    }

    // spin
    for (int i = 0; i < N_PARTICLES; i++){
        while (threads[i]->status == IDLE || threads[i]->status == RUNNNING){}
    }

    for (int i = 0; i < N_PARTICLES; i++){
        float xi_hat_float = 0;

        switch (threads[i]->status)
        {
        case ERROR:
            for (int j = 0; j < N_STEPS; j++){
                write_to_numpy_file(s->data, &xi_hat_float, FLOAT32);
            }
            break;
        case KILLED:
            for (int j = 0; j < threads[i]->data_size; j++){
                xi_hat_float = threads[i]->xdata[j];
                write_to_numpy_file(s->data, &xi_hat_float, FLOAT32);
            }
            break;
        }
    }
}


void teardown(char *note){
    write_json_metadata(N_PARTICLES, N_STEPS, note);
    close_numpy_files();
}
