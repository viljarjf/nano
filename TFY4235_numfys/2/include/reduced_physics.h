#ifndef BBM_REDUCED_PHYSICS_H
#define BBM_REDUCED_PHYSICS_H

#include "physics.h"
#include "constants.h"

/**
 * @brief Calculate the potential at point x at time t
 * 
 * @param x_hat Coordinate
 * @param t Time
 * @return double 
 * @note Uses reduced units
 */
double U_reduced(double x_hat, double t);

/**
 * @brief Calculate the force at point x at time t
 * 
 * @param x Coordinate
 * @param t Time
 * @return double 
 * @note Used reduced units
 */
double F_reduced(double x_hat, double t);


/**
 * @brief unmodulated saw potential
 * 
 * @param x coordinate
 * @return double 
 * @note Uses reduced units
 */
double U_r_reduced(double x_hat);

double F_r_reduced(double x_hat);

/**
 * @brief Calculate an number that should be much larger than delta t hat
 * 
 * @param reduced_constants pointer to reduced constants struct
 * @return double 
 */
double calc_delta_t_hat(reduced_constants_t *reduced_constants);

/**
 * @brief Calculate the probability of being at position x_hat
 * 
 * @param x_hat position, reduced
 * @return double 
 */
double reduced_bolzmann_distribution(double x_hat);

#endif
