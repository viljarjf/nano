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

typedef struct {
    FILE *fptr;
    NumpyType type;
} numpy_file_t;

/**
 * @brief Get the numpy file object
 * 
 * @param filename path to dest file, relative to project dir
 * @param shape shape of numpy array
 * @param n_dims dimensions of array
 * @param datatype 
 * @param file output pointer to resulting file object
 * @return numpy_file_t* 
 */
void get_numpy_file(
    char *filename, 
    int *shape, 
    size_t n_dims,
    NumpyType datatype,
    numpy_file_t *file
);

/**
 * @brief Close the file object
 * 
 * @param file 
 */
void close_numpy_file(numpy_file_t *file);

/**
 * @brief Write the value to the file 
 * 
 * @param fptr Pre-initialized numpy file
 * @param value Pointer to value to be written
 * @param type Datatype of the value
 * @note value must have same type as the file expects.
 * If not, nothing will be done
 */
void write_to_numpy_file(
    numpy_file_t *fptr, 
    void *value, 
    NumpyType type
);

#endif
