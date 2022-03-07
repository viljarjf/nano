#ifndef BBM_UTILS_H
#define BBM_UTILS_H

#include <stdio.h>

#define NUMPY_MAJOR_VERSION 1
#define NUMPY_MINOR_VERSION 0

typedef enum {
    FLOAT32,
    FLOAT64,
    INT32,
    INT64
} NumpyType;

/**
 * @brief Get the numpy file object
 * 
 * @param filename path to dest file, relative to project dir
 * @param shape shape of numpy array
 * @param n_dims dimensions of array
 * @param datatype 
 * @return FILE* 
 */
FILE *get_numpy_file(
    char *filename, 
    int *shape, 
    size_t n_dims,
    NumpyType datatype
);

#endif
