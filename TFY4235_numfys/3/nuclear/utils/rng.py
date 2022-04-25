"""Generate pseudorandom numbers"""

__ms_seed = 1234
__lc_seed = 2143

# https://en.wikipedia.org/wiki/Linear_congruential_generator#Parameters_in_common_use
__ms_m = 1 << 48    # 2^48
__ms_a = 0x5DEECE66D 
__ms_c = 11

def middle_square(seed: int = None, d: int = 4) -> int:
    """use the middle square method to generate a random number

    Args:
        seed (int): seed. If omitted, use the private variable `__seed`

    Returns:
        int: should have the same amount of digits as seed
    """
    # note: very bad
    global __ms_seed
    if seed is None:
        seed = __ms_seed

    s2 = seed ** 2
    res_str = ("0"*2*d + str(s2))
    res = int(res_str[-3*d//2:-d//2])
    __ms_seed = res
    return res

def linear_congruential(a: int = None, c: int = None, m: int = None) -> int:
    """Use the linear congruential method to generate pseudorandom numbers

    Args:
        a (int, optional): factor. Defaults to wikipedia value.
        c (int, optional): increment. Defaults to wikipedia value.
        m (int, optional): modulus. Defaults to wikipedia value.

    Returns:
        int: Pseudorandom number
    """
    if a is None:
        a = __ms_a
    if c is None:
        c = __ms_c
    if m is None:
        m = __ms_m
    global __lc_seed
    __lc_seed = (a*__lc_seed + c) % m
    return __lc_seed


def random():
    """sample a uniform distribution between 0 and 1.
    uses the linear congruential method with default parameters
    """
    return linear_congruential() / __ms_m
