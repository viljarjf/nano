def fact(x):
    res = 1
    for i in range(1,x+1):
        res *= i
    return res

def f(x, y):
    if y == 1:
        return 1
    elif y == 2:
        return x
    else:
        n = y - 1
        res = 1
        for i in range(n):
            res *= (x+i)
        return res / fact(n)

tests = [
    (1, 1, 1),
    (1, 2, 1),
    (3, 3, 6),
    (3, 5, 15),
    (9, 13, 125970),
    (13, 7, 18564),
    (15, 15, 40116600),
]

import time
start = time.time()
for _ in range(15):
    for x, y, solution in tests:
        found_solution = f(x, y)
        if solution != found_solution:
            print(
                f"Feilet for testen x={x} y={y}, resulterte i svaret"
                f" {found_solution} i stedet for {solution}."
            )
print(time.time() - start)

