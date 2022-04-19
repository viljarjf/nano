#ifndef BBM_BBM_H
#define BBM_BBM_H

#include "numpy_IO.h"
#include "euler.h"

typedef struct {
    numpy_file_t *data;
    numpy_file_t *timef;
    numpy_file_t *potential;
    numpy_file_t *bolzmann;
    numpy_file_t *tau;
    reduced_constants_t *reduced_constants;
} runtime_struct_t;


void setup(runtime_struct_t *s);


void run(runtime_struct_t *s);


void sweep_tau(runtime_struct_t *s, int n, double start, double end);


void teardown(char *note);


#endif
