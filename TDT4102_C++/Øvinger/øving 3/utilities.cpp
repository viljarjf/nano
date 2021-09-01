#include "utilities.h"
#include <cstdlib>
#include <ctime>



int randomWithLimits(int min, int max){
    int rand_num = rand();
    int diff = max-min;
    return min + (rand_num % diff);
}

