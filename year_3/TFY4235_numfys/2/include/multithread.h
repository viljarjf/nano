#ifndef BBM_MULTITHRED_H
#define BBM_MULTITHRED_H

#define N_THREADS 10
#define MAX_THREAD_ID 1000

typedef enum {
    RUNNNING,
    IDLE,
    KILLED,
    ERROR,
} thread_status_t;

typedef struct {
    int ID;
    thread_status_t status;
    double *xdata;
    double tn;
    int data_size;
    int buffer_size;
} thread_t;

thread_t *open_thread(int ID, int buffer_size);


#endif
