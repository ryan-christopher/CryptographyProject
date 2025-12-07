# crypto_project/crypto_utils.py

from typing import Any


def are_relatively_prime(x, y):
    """
    Gibt True zurück, wenn gcd(x, y) == 1.
    """
    if x < 0:
        x = -x
    if y < 0:
        y = -y
    gcd_val = find_gcd(max(x, y), min(x, y))
    return gcd_val == 1


def extended_gcd(m, n):
    """
    Erweiterter Euklid:
    Liefert (gcd, x, y) mit m*x + n*y = gcd.
    """
    old_r, r = int(m), int(n)
    old_s, s = 1, 0
    old_t, t = 0, 1

    while r != 0:
        quotient = old_r // r

        temp_r = r
        r = old_r - quotient * r
        old_r = temp_r

        temp_s = s
        s = old_s - quotient * s
        old_s = temp_s

        temp_t = t
        t = old_t - quotient * t
        old_t = temp_t

    # old_r ist gcd, old_s und old_t sind die Koeffizienten
    return old_r, old_s, old_t


def find_gcd(large_number, small_number):
    """
    Normaler Euklidischer Algorithmus.
    """
    large_number = int(large_number)
    small_number = int(small_number)
    remainder = large_number % small_number

    while remainder > 0:
        large_number = small_number
        small_number = remainder
        remainder = large_number % small_number

    return small_number


def is_prime(number):
    """
    Einfacher Primzahltest (deterministisch, für kleinere Zahlen ok).
    """
    number = int(number)
    if number <= 1:
        return False
    if number <= 3:
        return True
    if number % 2 == 0 or number % 3 == 0:
        return False

    i = 5
    while i * i <= number:
        if number % i == 0 or number % (i + 2) == 0:
            return False
        i += 6

    return True


def miller_rabin_test(n, rounds, rng: Any):
    """
    Probabilistischer Primzahltest (Miller-Rabin).
    """
    n = int(n)
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    m = n - 1
    r = 0
    while m % 2 == 0:
        m //= 2
        r += 1

    for _ in range(rounds):
        b = rng.random_in_range(2, n - 2)
        x = pow(b, m, n)

        if x == 1 or x == n - 1:
            continue

        found_minus_one = False
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                found_minus_one = True
                break

        if not found_minus_one:
            return False

    return True


def mod_inverse(a, m):
    """
    Modularer Inverser: a^(-1) mod m.
    Wirft RuntimeError, wenn gcd != 1.
    """
    a = int(a)
    m = int(m)
    gcd_val, x, _ = extended_gcd(a, m)
    if gcd_val != 1:
        raise RuntimeError("Modular inverse does not exist (gcd != 1)")

    result = x % m
    if result < 0:
        result += m
    return result


def mod_pow(base, exp, mod):
    """
    Schnelle Exponentiation: base^exp % mod.
    (Man könnte auch pow(base, exp, mod) nehmen.)
    """
    base = int(base) % int(mod)
    exp = int(exp)
    mod = int(mod)
    result = 1

    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp //= 2

    return result


def get_prime_factors(n):
    """
    Zerlegt n in seine (einzigartigen) Primfaktoren.
    """
    n = int(n)
    prime_factors = set()

    if n % 2 == 0:
        prime_factors.add(2)
        while n % 2 == 0:
            n //= 2

    i = 3
    while i * i <= n:
        if n % i == 0:
            prime_factors.add(i)
            while n % i == 0:
                n //= i
        i += 2

    if n > 1:
        prime_factors.add(n)

    return prime_factors


def is_primitive_root(b, p, prime_factors):
    """
    Prüft, ob b ein primitiver Wurzel modulo p ist.
    """
    b = int(b)
    p = int(p)

    for factor in prime_factors:
        exponent = (p - 1) // factor
        x = mod_pow(b, exponent, p)
        if x == 1:
            return False
    return True


def find_generator(p):
    """
    Findet eine primitive Wurzel modulo Primzahl p.
    """
    p = int(p)
    prime_factors = get_prime_factors(p - 1)

    b = 2
    while b < p:
        if is_primitive_root(b, p, prime_factors):
            return b
        b += 1

    raise RuntimeError("Could not find generator")
