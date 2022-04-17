#ifndef BBM_UTILS_H
#define BBM_UTILS_H


/**
 * @brief Check if val%mod is in the range [lower, upper)
 * 
 * @param val 
 * @param lower 
 * @param upper 
 * @param mod
 * @return bool
 */
int is_in_mod_range(
    double val, 
    double lower, 
    double upper, 
    double mod
    );

#endif