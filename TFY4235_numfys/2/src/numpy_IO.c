#include "numpy_IO.h"
#include "constants.h"
#include "string.h"
#include "errno.h"

static numpy_file_t* numpy_files[MAX_NUMPY_FILES];
static int n_numpy_files = 0;

static char folder[12] = "data/latest";

static int get_size(NumpyType t){
    switch (t)
    {
    case FLOAT32:
        return sizeof(float);
    case FLOAT64:
        return sizeof(double);
    case INT32:
        return sizeof(int);
    case INT64:
        return sizeof(long);
    default:
        break;
    }
}

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

file_status_t make_numpy_file(
    char *filename, 
    int *shape, 
    size_t n_dims,
    NumpyType datatype,
    numpy_file_t *file
){
    // check if we can make more files
    if (n_numpy_files >= MAX_NUMPY_FILES){
        return ERROR_MAX_FILES;
    }

    // open file
    char filepath[5 + strlen(folder) + strlen(filename) + 1];
    sprintf(filepath, "%s/%s.npy", folder, filename);
    file->fptr = fopen(filepath, "wb");
    
    if (file->fptr == NULL){
        return ERROR_FILE_CREATION_FAILED;
    }

    
    // write magic numpy header start
    fprintf(file->fptr, "\x93NUMPY");

    // write version
    unsigned char nv[2] = {NUMPY_MAJOR_VERSION, NUMPY_MINOR_VERSION};
    fwrite(nv, 1, 2, file->fptr);

    // get rest of header and its size
    __uint16_t h = 0;
    char *dict;
    get_dict(shape, n_dims, datatype, &dict, &h);

    // write last part of header
    fwrite(&h, sizeof(h), 1, file->fptr);
    fprintf(file->fptr, dict);

    file->type = datatype;

    numpy_files[n_numpy_files++] = file;
    return 0;
}

void write_to_numpy_file(numpy_file_t *fptr, void *value, NumpyType type){
    if (type == fptr->type){
        fwrite(value, get_size(type), 1, fptr->fptr);
    }
}

void write_json_metadata(int n_particles, int n_steps, char* note){
    const char* format = 
"{\n"
"    \"L\": %f,\n"
"    \"ALPHA\": %f,\n"
"    \"TAU\": %f,\n"
"    \"DELTA_U\": %f,\n"
"    \"KBT\": %f,\n"
"    \"R1\": %f,\n"
"    \"DELTA_T\": %f,\n"
"    \"N_PARTICLES\": %u,\n"
"    \"N_STEPS\": %u,\n"
"    \"NOTE\": \"%s\"\n"
"}\n";

    char filepath[14 + strlen(folder) + 1];
    sprintf(filepath, "%s/metadata.json", folder);
    FILE *fptr = fopen(filepath, "wb");
    fprintf(
        fptr, 
        format,
        constants->L,
        constants->ALPHA,
        constants->TAU,
        constants->DELTA_U,
        constants->KBT,
        constants->R1,
        constants->DELTA_T,
        n_particles,
        n_steps,
        note
    );
    fclose(fptr);
}

void close_numpy_files(){
    for(int i = 0; i < n_numpy_files; i++){
        fclose(numpy_files[i]->fptr);
        free(numpy_files[i]);
    }
    n_numpy_files = 0;
}
