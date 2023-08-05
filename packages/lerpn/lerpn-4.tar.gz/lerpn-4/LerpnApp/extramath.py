"""Extra mathematical functions."""

import cmath
import math

def degree_trig(func):
    """Create a unary trig operator that accepts degrees."""
    def wrapper(value):
        """Wrapper function: trig(degrees)"""
        value_deg = value * math.pi / 180
        return func(value_deg)
    return wrapper

def degree_invtrig(func):
    """Create a unary inverse trig operator that returns degrees.
    """
    def wrapper(value):
        """Wrapper function: rad2deg(trig(value))"""
        return func(value) * 180 / math.pi
    return wrapper

def autoc(fname):
    """Return a wrapper function that calls Call math.<fname> for floats and
    ints, cmath.<fname> for complex"""

    def wrapper(n, *args):
        """Wrapper function: math.fname(float), cmath.fname(complex)"""
        if isinstance(n, complex):
            return getattr(cmath, fname)(n, *args)
        else:
            return getattr(math, fname)(n, *args)
    return wrapper

def clamp(lower, n, upper):
    """Return n clamped to the range lower <= n <= upper"""

    return max(lower, min(n, upper))

# From https://code.activestate.com/recipes/66472/
# Originally by Dinu Gherman (first version) and Walter Brunswick (improved)
# Python Software Foundation license
def frange(end, start=0, inc=0):
    """A range function that accepts float increments."""

    if not start:
        start = end + 0.0
        end = 0.0
    else: end += 0.0

    if not inc:
        inc = 1.0
    count = int(math.ceil((start - end) / inc))

    L = [None] * count

    L[0] = end
    for i in range(1, count):
        L[i] = L[i-1] + inc
    return L
