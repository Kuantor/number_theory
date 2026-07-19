"""Tests for the GCD/LCM MVP (issue #2)."""
import math

import pytest

import number_theory as nt


def test_gcd_basic():
    assert nt.gcd(12, 18) == 6
    assert nt.gcd(1071, 462) == 21
    assert nt.gcd(17, 5) == 1


def test_gcd_zero_and_negatives():
    assert nt.gcd(0, 0) == 0
    assert nt.gcd(0, 9) == 9
    assert nt.gcd(9, 0) == 9
    assert nt.gcd(-12, 18) == 6
    assert nt.gcd(-12, -18) == 6


def test_gcd_matches_stdlib():
    for a in range(-30, 31):
        for b in range(-30, 31):
            assert nt.gcd(a, b) == math.gcd(a, b)


def test_gcd_bigint():
    a = 2 ** 512 * 3
    b = 2 ** 300 * 9
    assert nt.gcd(a, b) == math.gcd(a, b)


def test_lcm_basic():
    assert nt.lcm(4, 6) == 12
    assert nt.lcm(21, 6) == 42
    assert nt.lcm(0, 5) == 0
    assert nt.lcm(-4, 6) == 12


def test_lcm_matches_stdlib():
    for a in range(-20, 21):
        for b in range(-20, 21):
            assert nt.lcm(a, b) == math.lcm(a, b)


def test_extended_gcd_identity():
    for a in range(-25, 26):
        for b in range(-25, 26):
            g, x, y = nt.extended_gcd(a, b)
            assert g == math.gcd(a, b)
            assert a * x + b * y == g


def test_many():
    assert nt.gcd_many(12, 18, 24) == 6
    assert nt.lcm_many(4, 6, 8) == 24
    with pytest.raises(ValueError):
        nt.gcd_many()


def test_type_errors():
    for bad in (1.5, "3", None, True):
        with pytest.raises(TypeError):
            nt.gcd(bad, 2)
