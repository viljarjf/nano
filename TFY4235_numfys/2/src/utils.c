#include "utils.h"

static void get_dict(
    int *shape, 
    size_t n_dims, 
    NumpyType datatype,
    char **dict, 
    __uint16_t *dict_size
){
    int size = 0;
    char out_buffer[500]; // will be pruned later

    const char datatype_str[3];
    switch (datatype)
    {
    case FLOAT32:
        sprintf(datatype_str, "f4");
        break;
    case FLOAT64:
        sprintf(datatype_str, "f8");
        break;
    case INT32:
        sprintf(datatype_str, "i4");
        break;
    case INT64:
        sprintf(datatype_str, "i8");
        break;
    default:
        break;
    }
    size += sprintf(
        out_buffer + size, 
        "{'descr': '%s', 'fortran_order': False, 'shape': (",
        datatype_str);

    for (int i = 0; i < n_dims; i++){
        size += sprintf(
            out_buffer + size, 
            "%i, ",
            shape[i]);
    }
    size += sprintf(
        out_buffer + size - 2, 
        "), }") - 2;
    
    *dict = out_buffer;
    *dict_size = size;
}

FILE *get_numpy_file(
    char *filename, 
    int *shape, 
    size_t n_dims,
    NumpyType datatype
){
    // open file
    FILE *fptr = fopen(filename, "wb");

    // write magic numpy header start
    fprintf(fptr, "\x93NUMPY");

    // write version
    unsigned char nv[2] = {NUMPY_MAJOR_VERSION, NUMPY_MINOR_VERSION};
    fwrite(nv, 1, 2, fptr);

    // get rest of header and its size
    __uint16_t h = 0;
    char *dict;
    get_dict(shape, n_dims, datatype, &dict, &h);

    // write last part of header
    fwrite(&h, sizeof(h), 1, fptr);
    fprintf(fptr, dict);

    return fptr;
}