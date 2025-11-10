import sys
from typing import Tuple

#!/usr/bin/env python3
"""
Find integers x, y such that x*m + y*n = d where d is the smallest positive
integer representable as an integer combination of m and n (i.e. d = gcd(m, n)).

"""

def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """
    Return (g, x, y) such that a*x + b*y = g = gcd(a, b).
    """
    if b == 0:
        return (abs(a), 1 if a >= 0 else -1, 0)
    g, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return (g, x, y)

def main(argv):
    if len(argv) != 3:
        print("Usage: python {} m n".format(argv[0]))
        return 1
    try:
        m = int(argv[1])
        n = int(argv[2])
    except ValueError:
        print("m and n must be integers")
        return 1

    g, x, y = extended_gcd(m, n)
    # Ensure g is positive and representation matches g
    print(f"gcd({m}, {n}) = {g}")
    print(f"{x}*{m} + {y}*{n} = {x*m + y*n}")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))