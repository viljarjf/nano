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

extern const constants_t *constants;

#define PI          3.14159     // [~]
#define ETA         0.001       // [Pas]

#endif
