#include "multithread.h"
#include "euler.h"

#include <pthread.h>

static pthread_t pthreads[N_THREADS];

// thread_ids[ID] = index into pthreads
static int thread_ids[MAX_THREAD_ID];
static int thread_usage[N_THREADS];
static int n_ids = 0;
static int n_active_threads = 0;

// simple stack to queue thread creation
static thread_t *thread_queue[MAX_THREAD_ID];
static int head = 0;
static int tail = 0;

static thread_t * pop(){
    head %= MAX_THREAD_ID;
    if (tail % MAX_THREAD_ID == head){return NULL;}
    return thread_queue[head++];
}
static void push(thread_t * t){
    tail %= MAX_THREAD_ID;
    if ((head - tail) % MAX_THREAD_ID == 1){return -1;}
    thread_queue[tail++] = t;
}

// forward declare
static void *thread_func(void *thread);

// actually make the threads
static void create_thread(int thread_no, thread_t *t){
    int return_code = pthread_create(&pthreads[thread_no], NULL, *thread_func, t);
    if (!return_code){
        thread_usage[thread_no] = 1;
        thread_ids[t->ID] = thread_no;
    }
    else{
        // thread creation failed
        t->status = ERROR;
        free(t->xdata);
    }
}

// API, creates and enqueues threads
thread_t *open_thread(int ID, int buffer_size){
    if (ID >= MAX_THREAD_ID){
        return NULL;
    }
    double xdata[(const int)buffer_size];
    thread_t *thread = malloc(sizeof(thread_t));
    thread->ID = ID;
    thread->status = IDLE;
    thread->xdata = xdata;
    thread->tn = 0;
    thread->data_size = 0;
    thread->buffer_size = buffer_size;

    if (n_active_threads >= N_THREADS){
        push(thread);
    }
    else{
        create_thread(n_active_threads, thread);
        n_active_threads++;
    }
    n_ids++;
    return thread;
}

// define the func to run
static void *thread_func(void *thread){
    thread_t *t = (thread_t *)thread;
    t->status = RUNNNING;
    double xi_hat = 0;
    double ti = 0;
    for (int i = 0; i < t->buffer_size; i++){
        euler_scheme(&xi_hat, &ti);
        t->xdata[i] = xi_hat;
        t->data_size++;
    }
    // done
    t->tn = ti;
    t->status = KILLED;
    thread_usage[thread_ids[t->ID]] = 0;

    // start next thread if there are any in the queue
    thread_t *t_new = pop();

    if (t_new != NULL){
        create_thread(thread_ids[t->ID], t_new);
    }
    
    pthread_exit(NULL);
}

