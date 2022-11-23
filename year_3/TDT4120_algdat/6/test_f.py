
def f(x, y):
    if x < y:
        x, y = y, x
    if y == 1:
        return 1
    elif y == 2:
        return x
    else:
        n = y - 1
        res = 1
        for i in range(n):
            res *= (x+i) / (n - i)
        return round(res)

cache = {}
def f(x, y):
    if x < y:
        x, y = y, x
    key = (x, y)
    if cache.get(key) is not None:
        return cache[key]
    if x == 1 or y == 1:
        retval =  1
    else:
        retval =  f(x-1, y) + f(x, y-1)
    cache[key] = retval
    return retval


tests = [
    (1, 1, 1),
    (1, 2, 1),
    (3, 3, 6),
    (3, 5, 15),
    (9, 13, 125970),
    (13, 7, 18564),
    (15, 15, 40116600),
    (56, 167, 44153027595931414420018665050929843653518642490945992)
]

import time
start = time.time()
for _ in range(1000):
    cache = {}
    for x, y, solution in tests:
        found_solution = f(x, y)
        if solution != found_solution:
            print(
                f"Feilet for testen x={x} y={y}, resulterte i svaret"
                f" {found_solution} i stedet for {solution}."
            )
            print(f"{found_solution}\n{solution}")
print(time.time() - start)

