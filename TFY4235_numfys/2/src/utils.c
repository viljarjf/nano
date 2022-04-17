#include "utils.h"

int is_in_mod_range(double val, double lower, double upper, double mod){
    return (lower <= fmod(val, mod) && fmod(val, mod) < upper);
}
