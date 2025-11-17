# Naor–Reingold Pseudorandom-Bit
# ----------------------------------------------
# Erzeugt eine PRF-ähnliche Funktion f: {0,1}^n -> {0,1}.

import random

def pow_mod(x, e, n):
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
    small = [2,3,5,7,11,13,17,19,23,29]
    if n in small:
        return True
    if any(n % p == 0 for p in small):
        return False
    # Miller-Rabin
    m = n - 1
    r = 0
    while m % 2 == 0:
        m //= 2; r += 1
    for _ in range(k):
        b = random.randrange(2, n-1)
        x = pow_mod(b, m, n)
        if x == 1 or x == n-1: 
            continue
        ok = False
        for _ in range(r-1):
            x = (x*x) % n
            if x == n-1:
                ok = True
                break
        if not ok:
            return False
    return True

def gen_nbit_prime(bits):
    while True:
        # simple odd candidate
        cand = random.getrandbits(bits) | 1 | (1 << (bits-1))
        if is_probable_prime(cand):
            return cand

class NaorReingold:
    def __init__(self, n_bits=8):
        # 1) Fix n
        self.n = n_bits
        # 2) zwei n-Bit-Primzahlen p,q
        p = gen_nbit_prime(n_bits)
        q = gen_nbit_prime(n_bits)
        self.N = p * q
        # 4) 2n Zufallszahlen a_{i,0}, a_{i,1} in [1..N]
        self.a = [(random.randrange(1, self.N), random.randrange(1, self.N))
                  for _ in range(self.n)]
        # 5) g als Quadrat in Z_N^*
        #    wähle t mit gcd(t,N)=1 und setze g = t^2 mod N
        while True:
            t = random.randrange(2, self.N-1)
            if math.gcd(t, self.N) == 1:
                break
        self.g = pow_mod(t, 2, self.N)
        # 10) zufälliger r in {0,1}^n
        self.r = [random.getrandbits(1) for _ in range(self.n)]

    def _beta_n(self, v):
        # n-LSBs von v als Liste [b_{n-1},...,b_0] (oder anders – hier LSB->MSB Ordnung egal,
        # da nur Skalarprodukt mod 2 genutzt wird)
        return [(v >> i) & 1 for i in range(self.n)]

    def f(self, x_bits):
        # x_bits: Liste/Iterable aus 0/1 der Länge n
        S = 0
        for i, xb in enumerate(x_bits):
            xb = 1 if xb else 0
            S += self.a[i][xb]
        v = pow_mod(self.g, S, self.N)
        beta = self._beta_n(v)
        # Skalarprodukt mod 2
        s = 0
        for bi, ri in zip(beta, self.r):
            s ^= (bi & ri)
        return s

# Main function
if __name__ == "__main__":
    import math
    print("Naor–Reingold (gibt Bits f(x) für x in {0,1}^n)")
    n = int(input("n (z.B. 6 wie im Beispiel der Folien) = "))
    nr = NaorReingold(n_bits=n)
    # Beispiel: ein x abfragen
    xs = input(f"x als {n}-Bitfolge (z.B. 101011) = ").strip()
    x_bits = [1 if c == '1' else 0 for c in xs]
    print("f(x) =", nr.f(x_bits))
