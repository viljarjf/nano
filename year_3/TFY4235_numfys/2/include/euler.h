#ifndef BBM_EULER_H
#define BBM_EULER_H

#include "constants.h"
#include "reduced_physics.h"
#include "rng.h"

/**
 * @brief Implement the Euler scheme in eq. 2.9
 * 
 * @param x Coordinate, will be updated
 * @param t Time, will be updated
 * @param r Particle radius
 */
void euler_scheme(double *x_hat, double *t);

#endif
