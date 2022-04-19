#include "BBM.h"

int main(int argsc, char *argv[]){
    
    char header[33] = "################################";
    printf("%s\n#    Biased Brownian Motion    #\n%s\n", header, header);

    srand((unsigned)time());
    
    printf("Starting setup...\n");
    runtime_struct_t *t = malloc(sizeof(runtime_struct_t));
    setup(t);
    printf("Setup complete.\n");

    printf("Starting computation...\n");
    //run(t);
    sweep_tau(t, 1000, 1.0, 3.0);
    printf("Computation complete.\n");

    teardown(argv[1]);

    printf("%s\n#   Data generation complete   #\n%s\n", header, header);

    return 0;
}
