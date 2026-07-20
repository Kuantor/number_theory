"""number_theory — lightweight, dependency-free number theory.

The public API is re-exported from the compiled ``_core`` extension so that
the algorithms ship as a binary, not as readable source.
"""
from ._core import gcd, lcm, extended_gcd, gcd_many, lcm_many

__all__ = ["gcd", "lcm", "extended_gcd", "gcd_many", "lcm_many"]
__version__ = "0.2.0"
