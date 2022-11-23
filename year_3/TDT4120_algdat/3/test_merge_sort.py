#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

# De tilfeldig genererte testene er like for hver gang du kjører koden.
# Hvis du vil ha andre tilfeldig genererte tester, så endre dette nummeret.
random.seed(123)


def merge(A, p, q, r):
    n1 = q-p+1
    n2 = r-q
    L = A[p: p + n1] + [float("inf")] 
    R = A[q+1: q+1 + n2] + [float("inf")] 
    i = j = 0
    for k in range(p, r+1):
            if L[i] <= R[j]:
                A[k] = L[i]
                i += 1
            else:
                A[k] = R[j]
                j += 1

def merge_sort(A, p, r):
    if p < r:
        q = (p+r)//2
        merge_sort(A, p, q)
        merge_sort(A, q+1, r)
        merge(A, p, q, r)


def generate_merge_tests():
    # Noen håndskrevne merge-tester
    tests = [
        (([1], 0, 0, 0), [1]),
        (([1, 3, 2], 0, 0, 1), [1, 3, 2]),
        (([3, 1, 2], 0, 0, 1), [1, 3, 2]),
        (([1, 2, 1, 2], 0, 1, 3), [1, 1, 2, 2]),
        (([1, 2, 1, 2], 0, 1, 2), [1, 1, 2, 2]),
        (([1, 2, 1, 2], 1, 1, 3), [1, 1, 2, 2]),
        (([1, 2, 1, 2], 1, 1, 2), [1, 1, 2, 2]),
        (([1, 3, 1, 3, 1, 2, 4, 3], 2, 3, 6), [1, 3, 1, 1, 2, 3, 4, 3]),
        (
            ([99, 2, 3, 4, 5, 6, 7, 8, 7], 0, 0, 5),
            [2, 3, 4, 5, 6, 99, 7, 8, 7],
        ),
    ]

    # Noen tilfeldig-genererte merge-tester
    for i in range(10):
        p = random.randint(0, 5)
        q = p + random.randint(0, 5)
        r = q + random.randint(1, 5)
        test_case = (
            [random.randint(0, 10) for i in range(p)]
            + sorted([random.randint(0, 10) for i in range(q - p + 1)])
            + sorted([random.randint(0, 10) for i in range(r - q)])
            + [random.randint(0, 10) for i in range(random.randint(0, 5))],
            p,
            q,
            r,
        )
        answer = (
            test_case[0][:p]
            + sorted(test_case[0][p : r + 1])
            + test_case[0][r + 1 :]
        )
        tests.append((test_case, answer))

    return tests


# Tester merging
tests = generate_merge_tests()

for test_case, answer in tests:
    a, p, q, r = test_case
    student = a[:]
    merge(student, p, q, r)
    if student != answer:
        if len(a) < 20:
            response = (
                "Merge feilet for følgende input: "
                + "(a={:}, p={:}, q={:}, r={:}). ".format(a, p, q, r)
                + "Din output: {:}. Riktig output: {:}".format(student, answer)
            )
        else:
            response = "Merge feilet på input som er for langt til å vises her"
        print(response)
        break


def generate_merge_sort_tests():

    # Håndskrevne merge sort-tester
    tests = [
        (([], 0, -1), []),
        (([1], 0, 0), [1]),
        (([1, 3, 2], 0, 1), [1, 3, 2]),
        (([3, 1, 2], 0, 1), [1, 3, 2]),
        (([1, 2, 1, 2], 0, 3), [1, 1, 2, 2]),
        (([1, 2, 1, 2], 0, 2), [1, 1, 2, 2]),
        (([1, 2, 1, 2], 1, 3), [1, 1, 2, 2]),
        (([1, 2, 1, 2], 1, 2), [1, 1, 2, 2]),
        (([3, 1, 0, 5], 0, 3), [0, 1, 3, 5]),
        (([1, 3, 1, 3, 1, 2, 4, 3], 2, 6), [1, 3, 1, 1, 2, 3, 4, 3]),
        (([99, 2, 3, 4, 5, 6, 7, 8, 7], 0, 5), [2, 3, 4, 5, 6, 99, 7, 8, 7]),
        (([1, 0, 5], 7, 6), [1, 0, 5]),
        (([1, 0, 5], 7, 7), [1, 0, 5]),
        (([1, 0, 5], 1, 1), [1, 0, 5]),
    ]

    # Noen tilfeldige merge sort-tester
    for i in range(10):
        p = random.randint(0, 5)
        r = p + random.randint(0, 5)
        test_case = (
            [random.randint(0, 10) for i in range(r + random.randint(1, 5))],
            p,
            r,
        )
        answer = (
            test_case[0][:p]
            + sorted(test_case[0][p : r + 1])
            + test_case[0][r + 1 :]
        )
        tests.append((test_case, answer))

    return tests


tests = generate_merge_sort_tests()

# Tester mergesort
for test_case, answer in tests:
    a, p, r = test_case
    student = a[:]
    merge_sort(student, p, r)
    if student != answer:
        if len(a) < 20:
            response = (
                "Merge sort feilet for følgende input: "
                + "(a={:}, p={:}, r={:}). ".format(a, p, r)
                + "Din output: {:}. Riktig output: {:}".format(student, answer)
            )
        else:
            response = (
                "Merge sort feilet på input som "
                + "er for langt til å vises her"
            )
        print(response)
        break
