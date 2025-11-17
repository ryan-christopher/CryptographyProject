# Primitive Root Search
# --------------------------
# b ist primitive Wurzel mod p genau dann,
# wenn für alle Primteiler q von (p-1) gilt: b^((p-1)/q) != 1 (mod p).

def fast_exp_mod(x, e, n):
    # sehr einfache Square-and-Multiply
    x %= n
    Y = 1
    E = int(e)
    while E > 0:
        if E % 2 == 0:
            x = (x * x) % n
            E //= 2
        else:
            Y = (x * Y) % n
            E -= 1
    return Y

def trial_division_prime_factors(n):
    """Grobe Primfaktoren von n (nur Menge der Primteiler, Multiplik. egal)."""
    factors = set()
    d = 2
    while d * d <= n:
        if n % d == 0:
            factors.add(d)
            while n % d == 0:
                n //= d
        d += 1 if d == 2 else 2  # kleine Spar-Variante (nach 2 nur ungerade)
    if n > 1:
        factors.add(n)
    return factors

def is_primitive_root(b, p):
    """Testet mit Theorem: für alle q | (p-1) muss b^((p-1)/q) != 1 (mod p)."""
    if b % p == 0:
        return False
    phi = p - 1
    primes = trial_division_prime_factors(phi)
    for q in primes:
        if fast_exp_mod(b, phi // q, p) == 1:
            return False
    return True

def find_primitive_root(p):
    """Sucht eine primitive Wurzel mod p.
    Probiert erst ein paar übliche Kandidaten (2,3,5), dann linear weiter."""
    for b in [2, 3, 5]:
        if 1 < b < p and is_primitive_root(b, p):
            return b
    # notfalls weiterprobieren
    for b in range(2, p):
        if is_primitive_root(b, p):
            return b
    return None  # sollte bei primem p nie passieren

# Main function
if __name__ == "__main__":
    print("Primitive Root Search (mod p, p prim)")
    try:
        p = int(input("p = "))
    except ValueError:
        print("Bitte eine ganze Zahl eingeben.")
    else:
        if p < 3:
            print("p sollte eine Primzahl > 2 sein.")
        else:
            g = find_primitive_root(p)
            if g is None:
                print("Keine primitive Wurzel gefunden (unerwartet).")
            else:
                print(f"Primitive Wurzel modulo {p}: g = {g}")