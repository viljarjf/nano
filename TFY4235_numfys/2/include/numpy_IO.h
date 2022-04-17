#ifndef BBM_NUMPY_IO_H
#define BBM_NUMPY_IO_H

#include <stdio.h>
#include <stdlib.h>

#define NUMPY_MAJOR_VERSION     1
#define NUMPY_MINOR_VERSION     0
#define MAX_NUMPY_FILES         10

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

typedef enum {
    STATUS_OK,
    ERROR_MAX_FILES,
    ERROR_FILE_CREATION_FAILED
} file_status_t;

/**
 * @brief Get the numpy file object
 * 
 * @param filename path to dest file, relative to project dir
 * @param shape shape of numpy array
 * @param n_dims dimensions of array
 * @param datatype 
 * @param file output pointer to resulting file object
 * @return state 
 */
file_status_t make_numpy_file(
    char *filename, 
    int *shape, 
    size_t n_dims,
    NumpyType datatype,
    numpy_file_t *file
);

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

/**
 * @brief Close the file object
 * 
 * @param file 
 */
void close_numpy_files();


#endif
