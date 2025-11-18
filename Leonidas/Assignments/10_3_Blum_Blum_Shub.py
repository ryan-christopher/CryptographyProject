# Blum–Blum–Shub
# -------------------------------
# Baut n = p*q mit p ≡ q ≡ 3 (mod 4), dann s_{i+1} = s_i^2 (mod n), Bits = LSB(s_i).

import random
import math

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
        if x == 1 or x == n - 1:
            continue
        good = False
        for _ in range(r-1):
            x = (x * x) % n
            if x == n - 1:
                good = True
                break
        if not good:
            return False
    return True

def gen_prime_3mod4(bits):
    # n-Bit-Primzahl mit p ≡ 3 (mod 4)
    while True:
        p = random.getrandbits(bits) | 1 | (1 << (bits-1))
        if p % 4 != 3:
            p += (3 - p % 4)  # justieren auf 3 mod 4
        if is_probable_prime(p):
            return p

class BlumBlumShub:
    def __init__(self, bits=256):
        # zwei große Primzahlen p,q ≡ 3 (mod 4)
        p = gen_prime_3mod4(bits)
        q = gen_prime_3mod4(bits)
        self.n = p * q
        # seed s0 in Z_n^* (teilerfremd zu n)
        while True:
            s0 = random.randrange(2, self.n-1)
            if math.gcd(s0, self.n) == 1:
                break
        self.state = pow_mod(s0, 2, self.n)  # oft nimmt man s1 = s0^2 mod n

    def next_bit(self):
        # s_{i+1} = s_i^2 mod n, Ausgabe = LSB(s_{i+1})
        self.state = (self.state * self.state) % self.n
        return self.state & 1  # niedrigstes Bit

    def next_bits(self, k):
        out = 0
        for _ in range(k):
            out = (out << 1) | self.next_bit()
        return out

if __name__ == "__main__":
    print("Blum–Blum–Shub Zufalls-Bitgenerator")
    bits = int(input("Bitlänge für p und q (z.B. 64 für Demo) = "))
    bbs = BlumBlumShub(bits=bits)
    k = int(input("Wieviele Bits ausgeben? = "))
    val = bbs.next_bits(k)
    print(f"{k} Bits (als Zahl): {val}")