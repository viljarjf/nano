"""Generate pseudorandom numbers"""

__ms_seed = 1234
__lc_seed = 2143

def middle_square(seed: int = None, d: int = 4) -> int:
    """use the middle square method to generate a random number

    Args:
        seed (int): seed. If omitted, use the private variable `__seed`

    Returns:
        int: should have the same amount of digits as seed
    """
    # note: very bad
    global __seed
    if seed is None:
        seed = __seed

    s2 = seed ** 2
    res_str = ("0"*2*d + str(s2))
    res = int(res_str[-3*d//2:-d//2])
    __seed = res
    return res

def linear_congruential(a: float, c: float, m: float) -> float:
    global __lc_seed
    __lc_seed = (a*__lc_seed + c) % m
    return __lc_seed