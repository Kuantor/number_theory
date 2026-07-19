# cython: language_level=3
"""Compiled core of the number_theory package.

This module is written in Cython and compiled to a native extension
(``_core.pyd`` on Windows / ``_core.so`` elsewhere). The ``.pyx`` source is
**not** shipped in the built wheel, so the algorithms here are distributed as
a binary only.

All functions operate on Python ``int`` objects, so they keep Python's
arbitrary-precision arithmetic (correct for numbers of any size).
"""
from functools import reduce


def _as_int(x):
    # Reject bool explicitly: True/False are ints in Python but are almost
    # never what a caller means here.
    if isinstance(x, bool) or not isinstance(x, int):
        raise TypeError("expected int, got %s" % type(x).__name__)
    return x


def gcd(a, b):
    """Greatest common divisor of ``a`` and ``b`` (Euclidean algorithm).

    Always non-negative. ``gcd(0, 0)`` is ``0``.
    """
    a = _as_int(a)
    b = _as_int(b)
    if a < 0:
        a = -a
    if b < 0:
        b = -b
    while b:
        a, b = b, a % b
    return a


def lcm(a, b):
    """Least common multiple of ``a`` and ``b`` (non-negative).

    ``lcm(x, 0) == 0`` for any ``x``.
    """
    a = _as_int(a)
    b = _as_int(b)
    if a == 0 or b == 0:
        return 0
    r = a // gcd(a, b) * b
    return -r if r < 0 else r


def extended_gcd(a, b):
    """Extended Euclidean algorithm.

    Returns a tuple ``(g, x, y)`` such that ``a * x + b * y == g`` where
    ``g == gcd(a, b)`` and ``g`` is non-negative.
    """
    a = _as_int(a)
    b = _as_int(b)
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
    if old_r < 0:
        old_r, old_s, old_t = -old_r, -old_s, -old_t
    return (old_r, old_s, old_t)


def gcd_many(*nums):
    """GCD of two or more integers."""
    if not nums:
        raise ValueError("gcd_many() requires at least one integer")
    return reduce(gcd, nums)


def lcm_many(*nums):
    """LCM of two or more integers."""
    if not nums:
        raise ValueError("lcm_many() requires at least one integer")
    return reduce(lcm, nums)
