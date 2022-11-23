"""tests for the RNG algorithms"""

from nuclear.utils import rng

def test_random():
    for _ in range(10000):
        assert rng.random() <= 1
    