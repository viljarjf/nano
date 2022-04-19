#include "utils.h"

#include <math.h>

int is_in_range(double val, double lower, double upper){
    return ((lower <= val) && (val < upper));
}

int is_in_mod_range(double val, double lower, double upper, double mod){
    return is_in_range(fmod(val, mod), lower, upper);
}
