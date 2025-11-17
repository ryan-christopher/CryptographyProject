# Miller–Rabin Primtest
# --------------------------------------
# Prüft: ist n wahrscheinlich prim? (k = Anzahl zufälliger Basen)
# n-1 = 2^r * m (m odd), teste b^m ≡ 1 (mod n)
# oder b^{2^k m} ≡ -1 (mod n) für ein k in {0,...,r-1}.

import random

def pow_mod(x, e, n):
    # schnelles Potenzieren (Square-and-Multiply)
    x %= n
    y = 1
    while e > 0:
        if e & 1:
            y = (y * x) % n
        x = (x * x) % n
        e >>= 1
    return y

def is_probable_prime(n, k=8):
    if n < 2:
        return False
    # kleine Sonderfälle
    small_primes = [2,3,5,7,11,13,17,19,23,29]
    if n in small_primes:
        return True
    if any(n % p == 0 for p in small_primes):
        return False

    # schreibe n-1 = 2^r * m
    m = n - 1
    r = 0
    while m % 2 == 0:
        m //= 2
        r += 1

    # k Runden mit zufälliger Basis b
    for _ in range(k):
        b = random.randrange(2, n - 1)
        x = pow_mod(b, m, n)
        if x == 1 or x == n - 1:
            continue
        witness_found = True
        for _ in range(r - 1):
            x = (x * x) % n
            if x == n - 1:
                witness_found = False
                break
        if witness_found:
            return False  # sicher zusammengesetzt
    return True  # wahrscheinlich prim

if __name__ == "__main__":
    try:
        n = int(input("Zahl n testen: "))
        k = int(input("Runden k (z.B. 8): "))
    except ValueError:
        print("Bitte ganze Zahlen eingeben.")
    else:
        print("wahrscheinlich prim" if is_probable_prime(n, k) else "zusammengesetzt")
