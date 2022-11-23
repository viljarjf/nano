#ifndef BBM_CONSTANTS_H
#define BBM_CONSTANTS_H

typedef struct {
    double L;
    double ALPHA;
    double TAU;
    double DELTA_U;
    double KBT;
    double R1;
    double DELTA_T;
} constants_t;

typedef struct {
    double D;
    double DELTA_T_HAT;
} reduced_constants_t;

void update_reduced_constants();

constants_t *constants;
reduced_constants_t *reduced_constants;

#define PI              3.14159     // [~]
#define ETA             0.001       // [Pas]
#define ELECTRONVOLT    1.7022e-19  // [J]

#endif
