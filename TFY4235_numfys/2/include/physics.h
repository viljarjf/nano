#ifndef BBM_PHYSICS_H
#define BBM_PHYSICS_H

#include "constants.h"
/**
 * @brief Calculate the potential at point x at time t
 * 
 * @param x Coordinate
 * @param t Time
 * @return double 
 * @note Uses reduced units
 */
double U(double x, double t);

/**
 * @brief Calculate the force at point x at time t
 * 
 * @param x Coordinate
 * @param t Time
 * @return double 
 * @note Used reduced units
 */
double F(double x, double t);

/**
 * @brief is the potential on?
 * 
 * @param t Time
 * @return int 
 * @note Uses reduced units
 */
int f_t(double t);

/**
 * @brief unmodulated saw potential
 * 
 * @param x coordinate
 * @return double 
 * @note Uses reduced units
 */
double U_r(double x);

#endif
