#ifndef BBM_EULER_H
#define BBM_EULER_H

#include "constants.h"
#include "physics.h"
#include "rng.h"

/**
 * @brief Implement the Euler scheme in eq. 2.9
 * 
 * @param x Coordinate, will be updated
 * @param t Time, will be updated
 * @param r Particle radius
 * @return double Next coordinate
 */
double euler_scheme(double *x, double *t, double r);

/**
 * @brief Calculate an number that should be much larger than delta t
 * 
 * @param r Particle radius
 * @return double 
 */
double calc_delta_t(double r);

#endif
