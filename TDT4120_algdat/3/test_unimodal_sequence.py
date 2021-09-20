#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import sys
import numpy as np


# De tilfeldig genererte testene er like for hver gang du kjører koden.
# Hvis du vil ha andre tilfeldig genererte tester, så endre dette nummeret.
random.seed(123)

def find_maximum(x):
    # 2 reads for setup, 1 read per iteration
    # (2 reads for some iterations).
    # the search area is halved every iteration
    _a = x[0]
    _b = x[-1]
    _l = len(x)
    def cheat(a, b, a_i, b_i):
        halflen = (b_i - a_i + 1) // 2
        c = x[a_i + halflen]
        if halflen <= 1:
            return max(a, b, c)
        if (a > c) and (a > b):
            return cheat(a, c, a_i, a_i + halflen)
        elif (a < b) and (c < b):
            return cheat(c, b, a_i + halflen, b_i)
        else:
            if x[a_i + halflen + 1] > c:
                return cheat(c, b, a_i + halflen, b_i)
            else:
                return cheat(a, c, a_i, a_i + halflen)
    return cheat(_a, _b, 0, _l - 1)

# Noen håndskrevne tester
tests = [
    ([1], 1),
    ([1, 3], 3),
    ([3, 1], 3),
    ([1, 2, 1], 2),
    ([1, 0, 2], 2),
    ([2, 0, 1], 2),
    ([0, 2, 1], 2),
    ([0, 1, 2], 2),
    ([2, 1, 0], 2),
    ([2, 3, 1, 0], 3),
    ([2, 3, 4, 1], 4),
    ([2, 1, 3, 4], 4),
    ([4, 2, 1, 3], 4),
]


def generate_random_test_case(length, max_value):
    test = random.sample(range(max_value), k=length)
    m = max(test)
    test.remove(m)
    t = random.randint(0, len(test))
    test = sorted(test[:t]) + [m] + sorted(test[t:], reverse=True)
    t = random.randint(0, len(test))
    test = test[t:] + test[:t]
    return (test, m)


def test_student_maximum(test_case, answer):
    student = find_maximum(test_case)
    if student != answer:
        if len(test_case) < 20:
            response = (
                "'Find maximum' feilet for følgende input: "
                + "(x={:}). Din output: {:}. ".format(test_case, student)
                + "Riktig output: {:}".format(answer)
            )
        else:
            response = (
                "Find maximum' feilet på input som er "
                + "for langt til å vises her"
            )
        print(response)
        sys.exit()

def run_test():
    # Testing student maximum on custom made tests
    for test_case, answer in tests:
        test_student_maximum(test_case, answer)

    # Testing student maximum on random test cases
    for i in range(40):
        test_case, answer = generate_random_test_case(random.randint(1, 100), 100)
        test_student_maximum(test_case, answer)

def gen_x(n):
    res = [i for i in range(n)]
    rev = random.randint(0, n-1)
    mov = random.randint(0, n-1)
    if rev%2:
        res[rev:] = res[rev:][::-1]
        res = res[mov:] + res[:mov]
        return res
    else:
        res[:rev] = res[:rev][::-1]
        res = res[mov:] + res[:mov]
        return res
test_gen = gen_x(20)
import time
from matplotlib import pyplot as plt
def big_o_test():
    x = []
    y = []
    for n in np.linspace(6000000, 8000000, num = 1000, dtype = int):
        _x = gen_x(n)
        start = time.time()
        for _ in range(10):
            find_maximum(_x)
        y.append(time.time() - start)
        x.append(n)
    avg = [sum(y[max(0, i-10):i+1])/min(i+1, 10) for i in range(len(y))]
    avg2 = [sum(y[max(0, i-30):i+1])/min(i+1, 30) for i in range(len(y))]
    plt.plot(x, y)
    plt.plot(x, avg)
    plt.plot(x, avg2)
    #plt.plot(x, [1.53*np.log2(i) for i in x])
    #plt.legend(["real", "max"])#, "under", "over"])
    plt.show()

if __name__ == "__main__":
    big_o_test()
    #find_maximum(generate_random_test_case(6000, 6000)[0])
    run_test()