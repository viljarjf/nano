# !/usr/bin/python3
# coding=utf-8


class Queue:

    # Simple testing suggests using builtins 
    # (append and pop) is faster than keeping
    # track of indices manually. 
    # Therefore, I eventually landed on the Queue_cheat-class
    # for final delivery

    def __init__(self, max_size):
        self.queue = [None] * max_size
        self.head = -1
        self.tail = -1
        self.max_size = max_size

    def enqueue(self, value):
        self.head += 1
        if self.head == self.tail:
            raise IndexError("Queue is full")
        self.queue[self.head % self.max_size] = value

    def dequeue(self):
        if self.head == self.tail:
            raise IndexError("Queue is empty")
        self.tail += 1
        return self.queue[self.tail % self.max_size]
    
    def __str__(self):
        return "Queue"

class Queue_cheat:

    def __init__(self, max_size):
        self.queue = []
        self.max_size = max_size + 1
        self.len = 0

    def enqueue(self, value):
        self.len += 1
        if self.len == self.max_size:
            self.len -= 1
            raise IndexError("Queue is full")
        self.queue.append(value)

    def dequeue(self):
        self.len -= 1
        if (self.len + 1):
            return self.queue.pop(0)
        self.len += 1
        raise IndexError("Queue is empty")

    def __str__(self):
        return "Queue_cheat"
        
import numpy as np
class Queue_numpy:

    def __init__(self, max_size):
        self.queue = np.zeros(max_size)
        self.head = -1
        self.tail = -1
        self.max_size = max_size

    def enqueue(self, value):
        self.head += 1
        if self.head == self.tail:
            raise IndexError("Queue is full")
        self.queue[self.head % self.max_size] = value

    def dequeue(self):
        if self.head == self.tail:
            raise IndexError("Queue is empty")
        self.tail += 1
        return self.queue[self.tail % self.max_size]

    def __str__(self):
        return "Queue_numpy"

from numba import njit

@njit
def push(q, h, m, v):
    q[h%m]=v

@njit
def pop(q, t, m):
    return q[t%m]

class Queue_numba:

    def __init__(self, max_size):
        self.queue = np.zeros(max_size)
        self.head = -1
        self.tail = -1
        self.max_size = max_size

    def enqueue(self, value):
        self.head += 1
        if self.head == self.tail:
            raise IndexError("Queue is full")
        push(self.queue, self.head, self.max_size, value)

    def dequeue(self):
        if self.head == self.tail:
            raise IndexError("Queue is empty")
        self.tail += 1
        return pop(self.queue, self.tail, self.max_size)
    
    def __str__(self):
        return "Queue_numba"

def tester(queue_class, values, sequence, max_size):
    """
    Tester en oppgitt sekvens av operasjoner og sjekker at verdiene
    (values) kommer ut i riktig rekkefølge.
    """
    index = 0
    queue = queue_class(max_size)
    output = []
    for action in sequence:
        if action == "enqueue":
            queue.enqueue(values[index])
            index += 1
        elif action == "dequeue":
            output.append(queue.dequeue())

    if output != values:
        print(
            "Feilet for følgende sekvens av operasjoner "
            + "'{:}' med verdiene ".format(", ".join(sequence))
            + "'{:}' og maksimal størrelse".format(", ".join(map(str, values)))
            + "'{:}'".format(max_size)
        )
        return True
    return False


tests = (
    (
        [1, 7, 3],
        ("enqueue", "dequeue", "enqueue", "dequeue", "enqueue", "dequeue"),
        3,
    ),
    (
        [1, 7, 3],
        ("enqueue", "dequeue", "enqueue", "dequeue", "enqueue", "dequeue"),
        1,
    ),
    (
        [-1, 12, 0, 99],
        (
            "enqueue",
            "enqueue",
            "dequeue",
            "dequeue",
            "enqueue",
            "enqueue",
            "dequeue",
            "dequeue",
        ),
        2,
    ),
    (
        [-1, 12, 0, 99],
        (
            "enqueue",
            "enqueue",
            "dequeue",
            "enqueue",
            "dequeue",
            "enqueue",
            "dequeue",
            "dequeue",
        ),
        2,
    ),
    (
        [-1, 12, 0, 99],
        (
            "enqueue",
            "enqueue",
            "enqueue",
            "enqueue",
            "dequeue",
            "dequeue",
            "dequeue",
            "dequeue",
        ),
        4,
    ),
    (
        [i for i in range(1000)],
        tuple(["enqueue"]*1000 + ["dequeue"]*1000),
        1000,
    ),
)

import time
def run_test(queue_class) -> bool:

    n_tests = 100000
    start = time.time()
    for _ in range(n_tests):
        for values, sequence, max_size in tests:
            tester(queue_class, values, sequence, max_size)
    print(f"{str(queue_class)}: {time.time() - start :.2f}s")
    

run_test(Queue)
run_test(Queue_cheat)
run_test(Queue_numpy)
run_test(Queue_numba)