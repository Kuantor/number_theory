"""Command-line interface for number_theory.

Examples::

    number-theory gcd 12 18 24
    number-theory lcm 4 6 8
    number-theory egcd 240 46
    python -m number_theory gcd 1071 462
"""
import argparse
import sys

from . import __version__, extended_gcd, gcd_many, lcm_many


def build_parser():
    parser = argparse.ArgumentParser(
        prog="number-theory",
        description="GCD / LCM via the Euclidean algorithm.",
    )
    parser.add_argument(
        "--version", action="version", version="number_theory %s" % __version__
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_gcd = sub.add_parser("gcd", help="greatest common divisor of two or more integers")
    p_gcd.add_argument("numbers", metavar="N", type=int, nargs="+")

    p_lcm = sub.add_parser("lcm", help="least common multiple of two or more integers")
    p_lcm.add_argument("numbers", metavar="N", type=int, nargs="+")

    p_eg = sub.add_parser("egcd", help="extended gcd: prints 'g x y' with a*x + b*y = g")
    p_eg.add_argument("a", type=int)
    p_eg.add_argument("b", type=int)

    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.command == "gcd":
        print(gcd_many(*args.numbers))
    elif args.command == "lcm":
        print(lcm_many(*args.numbers))
    elif args.command == "egcd":
        g, x, y = extended_gcd(args.a, args.b)
        print("%d %d %d" % (g, x, y))
    return 0


if __name__ == "__main__":
    sys.exit(main())
