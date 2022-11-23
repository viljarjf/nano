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

/**
 * @brief Calculate an number that should be much larger than delta t
 * 
 * @return double 
 */
double calc_delta_t();

/**
 * @brief Calculate the probability of being in energy U
 * 
 * @param U energy
 * @return double 
 */
double bolzmann_distribution_potential(double U);

/**
 * @brief Calculate the probability of being at position x
 * 
 * @param x position
 * @return double 
 */
double bolzmann_distribution_position(double x);

#endif
