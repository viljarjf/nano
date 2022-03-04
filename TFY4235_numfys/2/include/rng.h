#ifndef BBM_RNG_H
#define BBM_RNG_H

/**
 * @brief sample from a standard normal distribution
 * 
 * @return double 
 */
double rng();

/**
 * @brief Write n random numbers to a file, to verify the distribution
 * 
 * @param n 
 */
void write_rng_to_file(int n);

#endif
