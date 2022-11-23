#include "constants.h"

void update_reduced_constants(){
    double gamma = 6*PI*ETA*constants->R1;
    double omega = constants->DELTA_U / (gamma * constants->L*constants->L);
    reduced_constants->D            = constants->KBT / constants->DELTA_U;
    reduced_constants->DELTA_T_HAT  = omega * constants->DELTA_T;
}
