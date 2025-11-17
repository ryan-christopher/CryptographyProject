# Fast Exponentiation (Square-and-Multiply)
# --------------------------------------------------------
# Berechnet (x**e) mod n mit den Zuständen (x, e, Y).
# Regeln:
#   - wenn e gerade:   x <- (x*x) mod n,  e <- e//2
#   - wenn e ungerade: Y <- (x*Y) mod n,  e <- e-1
# Ergebnis: Y

def fast_exp_mod(x, e, n):
    if e < 0:
        raise ValueError("e muss >= 0 sein.")
    if n <= 0:
        raise ValueError("n muss > 0 sein.")

    x = x % n   # erst auf den Rest reduzieren
    Y = 1 % n
    E = int(e)

    while E > 0:
        if E % 2 == 0:
            # e ist gerade: Basis quadrieren, e halbieren
            x = (x * x) % n
            E = E // 2
        else:
            # e ist ungerade: Y mit x multiplizieren, e um 1 verringern
            Y = (x * Y) % n
            E = E - 1

    return Y


# Main function
if __name__ == "__main__":
    print("Fast Exponentiation: berechne (x^e) mod n")
    try:
        x = int(input("x = "))
        e = int(input("e (>= 0) = "))
        n = int(input("n (> 0) = "))
    except ValueError:
        print("Bitte ganze Zahlen eingeben.")
    else:
        val = fast_exp_mod(x, e, n)
        print(f"\nErgebnis: {x}^{e} mod {n} = {val}")