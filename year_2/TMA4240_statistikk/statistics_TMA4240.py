import math

verbose = False

def factorial(n: int)-> int:
    if n == 0:
        return 1
    elif n < 0:
        raise ValueError("The factorial of a negative integer is undefined")
    s = 1
    for i in range(1, n+1):
        s *= i
    return i

def average(l: list)-> float:
    avg = sum(l)/len(l)
    if verbose:
        print("The average value of\n", l, "\nis:\n", avg)
    return avg

def median(l: list)-> float:
    l.sort()
    n = (len(l)-1)/2
    a = math.floor(n)
    b = math.ceil(n)
    med = 0.5*(l[a] + l[b])
    if verbose:
        print("The median of\n", l, "\nis:\n", med)
    return med

def standard_deviation(l: list, verbose_override = False)-> float:
    s = average(l)
    tmp_sum = 0
    for i in l:
        tmp_sum += (i-s)**2
    std = math.sqrt(tmp_sum/(len(l)-1))
    if verbose and not verbose_override:
        print("The sample standard deviation of\n", l, "\nis:\n", std)
    return std

def variance(l: list)-> float:
    v = standard_deviation(l, verbose_override = True)**2
    if verbose:
        print("The variance of\n", l, "\nis\n", v)
    return v
