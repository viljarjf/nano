#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import base64
import sys
from typing import Tuple

# De tilfeldig genererte testene er like for hver gang du kjører koden.
# Hvis du vil ha andre tilfeldig genererte tester, så endre dette nummeret.
random.seed(123)

# Minimalisert kode for å verifisere at svaret er riktig. Kan ignoreres.
exec(
    base64.b64decode(
        "ZGVmIGExMjMoeCx4MCx5MCx4MSx5MSk6Cg"
        + "lBPWZsb2F0KCdpbmYnKQoJZm9yIEIgaW4g"
        + "cmFuZ2UoeDAseDErMSk6CgkJZm9yIEMgaW"
        + "4gcmFuZ2UoeTAseTErMSk6QT1taW4oQSx4"
        + "W0JdW0NdKQoJcmV0dXJuIEEKZGVmIGJydX"
        + "RlZm9yY2UoeCk6CglBPTAKCWZvciBCIGlu"
        + "IHJhbmdlKGxlbih4KSk6CgkJZm9yIEMgaW"
        + "4gcmFuZ2UobGVuKHhbMF0pKToKCQkJZm9y"
        + "IEQgaW4gcmFuZ2UoQixsZW4oeCkpOgoJCQ"
        + "kJZm9yIEUgaW4gcmFuZ2UoQyxsZW4oeFsw"
        + "XSkpOkE9bWF4KEEsKEQtQisxKSooRS1DKz"
        + "EpKmExMjMoeCxCLEMsRCxFKSkKCXJldHVybiBB"
    )
)

#cache = {}
def largest_cuboid(depthmap):
    # This is theta(n^4), and as such not fast enough
    
    n = len(depthmap)

    def find_largest_rectangle(slice):
        """
        slice: 2D arr, dtype bool, true -> allowed
        """
        #_hash = int("".join([str(j+0) for i in slice for j in i]), base = 2)
        #if _hash in cache:
        #    return cache[_hash]
        aux_arr = [[0 for _ in range(n)] for __ in range(n)]

        # find how long each point can see in x-axis
        for i in range(n):
            for j in range(n):
                ind = j
                n_x = 0
                while ind < n and slice[i][ind]:
                    n_x += 1
                    ind += 1
                aux_arr[i][j] = n_x

        # basically, find the largest rectangle that fits 
        # with (i,j) as top left corner.
        # skip points that guarantees smaller rectangles
        # than alreasy discovered

        res = max([j for i in aux_arr for j in i])
        for i in range(n):
            for j in range(n):
                n_x  = aux_arr[i][j]
                if n_x:
                    cur_n_x = n_x
                    for k in range(i+1, n):
                        n_x_next = aux_arr[k][j]
                        if n_x_next <= cur_n_x:
                            aux_arr[k][j] = 0

                        cur_n_x = n_x_next if n_x_next < cur_n_x else cur_n_x

                        new = (k-i + 1) * cur_n_x
                        if new > res:
                            res = new
            
        #cache[_hash] = res
        return res

    cur_max = 0
    for y in range(n):
        for x in range(n):
            depth = depthmap[y][x]
            new = find_largest_rectangle([[depthmap[i][j] >= depth for j in range(n)] for i in range(n)])*depth
            if new > cur_max:
                cur_max = new
    return cur_max

def _largest_cuboid(depthmap):
    n = len(depthmap)

    def get_depth(y, x0, x1):
        return min(depthmap[y][x0:x1])
        
    def largest_rect(slice):
        """
        start, end, depth
        """
        res = slice.copy()
        for i, depth in enumerate(slice):
            pass

def generate_random_test_case(length, max_value):
    test_case = [
        [random.randint(0, max_value) for i in range(length)]
        for j in range(length)
    ]
    return test_case, bruteforce(test_case)


def test_student_algorithm(test_case, answer):
    student = largest_cuboid(test_case)
    if student != answer:
        if len(test_case) < 4:
            response = "Koden feilet for følgende input: (x={:}).".format(
                test_case
            ) + " Din output: {:}. Riktig output: {:}".format(student, answer)
        else:
            response = "Koden feilet på input som er for langt til å vises her"
        print(response)
        sys.exit()

def run_tests():
    # Some håndskrevne tester
    tests = [
        ([[5, 5, 0], [2, 2, 5], [8, 5, 3]], 12),
        #([[2,2,2],[2,2,2],[2,1,1]], 12),
        #([[1]], 1),
        ([[1, 1], [2, 1]], 4),
        ([[1, 1], [5, 1]], 5),
        ([[0, 0], [0, 0]], 0),
        ([[10, 0], [0, 10]], 10),
        ([[10, 6], [5, 10]], 20),
        ([[100, 100], [40, 55]], 200),
    ]

    # Tester funksjonen på håndskrevne tester
    for test_case, answer in tests:
        test_student_algorithm(test_case, answer)

    # Tester funksjonen på tilfeldig genererte tester
    for i in range(20):
        test_case, answer = generate_random_test_case(random.randint(1, 3), 10)
        test_student_algorithm(test_case, answer)
    for i in range(10):
        test_case, answer = generate_random_test_case(
            random.randint(1, 20), 100000
        )
        test_student_algorithm(test_case, answer)

import big_o
def big_o_check():
    print(big_o.big_o(
        largest_cuboid, 
        lambda n: [[random.randint(1, 1000) for _ in range(n)] for __ in range(n)], 
        max_n = 25, 
        min_n = 5, 
        n_repeats = 20
        )[0])
    
import pickle, time
if __name__ == "__main__":
    # big_o_check()
    start = time.time()
    big_o_check()
    print(time.time() - start)
    #code = pickle.dumps(cache).encode("base64", "strict")
    #print(code)