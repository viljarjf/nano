#!/usr/bin/python3
# coding=utf-8

import random
def k_largest(A, k):

    def find_k_largest(arr: list, l, k):
        if k == 0:
            return []
        elif l <= 1:
            return arr
        p = arr.pop(random.randint(0, l-1))
        aux_min = []
        aux_max = []
        for i in range(l-1):
            if arr[i] > p:
                aux_max.append(arr[i])
            else:
                aux_min.append(arr[i])
        lm = len(aux_max)
        if lm == k:
            return aux_max
        elif lm == k-1:
            return [p] + aux_max
        elif lm > k:
            return find_k_largest(aux_max, lm, k)
        else:
            return aux_max + [p] + find_k_largest(aux_min, l - lm - 1, k - lm  - 1)
    
    return find_k_largest(A, len(A), k)
            


# Sett med tester.
tests = [
    (([], 0), []),
    (([1], 0), []),
    (([1], 1), [1]),
    (([1, 2], 1), [2]),
    (([-1, -2], 1), [-1]),
    (([-1, -2, 3], 2), [-1, 3]),
    (([1, 2, 3], 2), [2, 3]),
    (([3, 2, 1], 2), [2, 3]),
    (([3, 3, 3, 3], 2), [3, 3]),
    (([4, 1, 3, 2, 3], 2), [3, 4]),
    (([4, 5, 1, 3, 2, 3], 4), [3, 3, 4, 5]),
    (([9, 3, 6, 1, 7, 3, 4, 5], 4), [5, 6, 7, 9]),
]

for test, solution in tests:
    A, k = test
    student_answer = k_largest(A[:], k)
    if type(student_answer) != list:
        print("Metoden må returnere en liste")
    else:
        student_answer.sort()
        if student_answer != solution:
            print(
                "Feilet for testen {:}, resulterte i listen ".format(test)
                + "{:} i stedet for {:}.".format(student_answer, solution)
            )
