#include "constants.h"

void get_reduced_constants(reduced_constants_t *reduced_constants, constants_t *constants){
    double gamma = 6*PI*ETA*constants->R1;
    double omega = constants->DELTA_U / (gamma * constants->L*constants->L);
    
    reduced_constants->D            = constants->KBT / constants->DELTA_U;
    reduced_constants->DELTA_T_HAT  = omega * constants->DELTA_T;
}
