# Baby-step / Giant-step
# ---------------------------------------
# Gegeben p (prim), Generator b, Ziel a aus Z_p^x.
# Finde l mit b^l ≡ a (mod p), 0 <= l < p-1.
#
# Schritte:
#   m = ceil(sqrt(n)) mit n = p-1
#   Tabelle der Baby-steps: b^j (0 <= j < m)
#   c = b^{-m}  (ein "großer Schritt" rückwärts)
#   x = a; für i=0..m:
#       falls x in Baby-Tabelle: l = i*m + j
#       sonst: x = x * c (mod p)

def egcd(a, b):
    # sehr einfacher erweiterter Euklid (für Inverses)
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
    return old_r, old_s, old_t  # gcd, x, y

def inv_mod(a, n):
    g, x, _ = egcd(a % n, n)
    if g != 1:
        raise ValueError("Kein Inverses vorhanden.")
    return x % n

def fast_exp_mod(x, e, n):
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

def baby_step_giant_step(p, b, a):
    """Gibt l mit b^l ≡ a (mod p) zurück, oder None falls nicht gefunden."""
    n = p - 1  # Ordnung von Z_p^x
    # m = ceil(sqrt(n))
    m = int(n**0.5)
    if m * m < n:
        m += 1

    # Baby-steps: b^j für j=0..m-1
    baby = {}
    val = 1  # b^0
    for j in range(m):
        # nur erstes Auftreten speichern (kleinstes j)
        if val not in baby:
            baby[val] = j
        val = (val * b) % p

    # c = b^{-m}
    c = inv_mod(fast_exp_mod(b, m, p), p)

    # Giant-steps: a * c^i
    x = a % p
    for i in range(m + 1):  # +1 als kleine Sicherheitsmarge
        if x in baby:
            j = baby[x]
            l = i * m + j
            if l < n:
                return l
        x = (x * c) % p

    return None

# Main function
if __name__ == "__main__":
    print("Baby-step / Giant-step in Z_p^x (p prim)")
    try:
        p = int(input("p = "))
        b = int(input("Generator b = "))
        a = int(input("Ziel a (b^l ≡ a mod p) = "))
    except ValueError:
        print("Bitte ganze Zahlen eingeben.")
    else:
        if p <= 2:
            print("p sollte eine Primzahl > 2 sein.")
        else:
            l = baby_step_giant_step(p, b, a)
            if l is None:
                print("Kein Logarithmus gefunden (b war evtl. kein Generator).")
            else:
                print(f"log_b(a) = l  mit  {b}^{l} ≡ {a} (mod {p})")