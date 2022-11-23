#!/usr/bin/python3
# coding=utf-8
k = 27
def counting_sort(keys, arr, output):
        C = [0 for _ in range(k)]
        for key in keys:
            C[key] += 1
        C = [sum(C[:i+1])-1 for i in range(k)]
        for key, a in zip(reversed(keys), reversed(arr)):
            output[C[key]] = a
            C[key] -= 1

def flexradix(A: list, d: int):

    aux = [0]*len(A)
    for ind in range(d).__reversed__():
        keys = [ord((s + "`"*d)[ind]) - 96 for s in A]
        counting_sort(keys, A, aux)
        A, aux = aux, A
    return A

import random
def generate_testcase(d, n):
    chars = "qwertyuiopasdfghjklzxcvbnm"
    res = []
    for _ in range(n):
        res.append("".join(random.choices(chars, k = random.randint(1, d))))
    return res

def test_big_o(n_0, n_1):
    diff = (n_1-n_0)//100
    d = 20
    t = []
    ns = []
    for n in range(n_0, n_1, diff):
        case = generate_testcase(d, n)
    #    start = time.time()
        flexradix(case, d)
        flexradix(case, d)
        flexradix(case, d)
    #    t.append(time.time() - start)
    #    ns.append(n)
    #plt.plot(ns, t)
    #plt.show()

#testcase = generate_testcase(20, 100)
#[print(i) for i in flexradix(testcase, 20)]

test_big_o(5000, 10000)


tests = (
    (([
        "aaaa",
        "aaab",
        "aaba",
        "abaa",
        "baaa"
    ], 4),["aaaa","aaab","aaba","abaa","baaa"]),
    (([], 1), []),
    ((["a"], 1), ["a"]),
    ((["a", "b"], 1), ["a", "b"]),
    ((["b", "a"], 1), ["a", "b"]),
    ((["ba", "ab"], 2), ["ab", "ba"]),
    ((["b", "ab"], 2), ["ab", "b"]),
    ((["ab", "a"], 2), ["a", "ab"]),
    ((["abc", "b"], 3), ["abc", "b"]),
    ((["abc", "b"], 4), ["abc", "b"]),
    ((["abc", "b", "bbbb"], 4), ["abc", "b", "bbbb"]),
    ((["abcd", "abcd", "bbbb"], 4), ["abcd", "abcd", "bbbb"]),
    ((["a", "b", "c", "babcbababa"], 10), ["a", "b", "babcbababa", "c"]),
    ((["a", "b", "c", "babcbababa"], 10), ["a", "b", "babcbababa", "c"]),
)

for test, solution in tests:
    student_answer = flexradix(test[0], test[1])
    if student_answer != solution:
        print(
            "Feilet for testen {:}, resulterte i listen ".format(test)
            + "{:} i stedet for {:}.".format(student_answer, solution)
        )
