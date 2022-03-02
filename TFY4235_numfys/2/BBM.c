#include <stdio.h>
#include "rng.h"
#include "stdlib.h"

int main(int argsc, char *argv[]){
    // based
    printf("Biased Brownian Motion\n");
    srand((unsigned) time());

    // write a bunch of random numbers to file for easy plotting in python
    // to verify the distribution
    FILE *fptr = fopen("randnums.txt", "w");

    for (int i = 0; i < 10000; i++){
        fprintf(fptr, "%f\n", rng());
    }
    fclose(fptr);
    
    return 0;
}
