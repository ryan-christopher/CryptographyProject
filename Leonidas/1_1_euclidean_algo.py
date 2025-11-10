def gcd(a, b):
    """Berechnet den größten gemeinsamen Teiler von a und b
    mit dem iterativen euklidischen Algorithmus.
    a und b dürfen auch negativ sein; wir arbeiten mit Beträgen."""
    a = abs(a)
    b = abs(b)

    print("== Euclidean Algorithmus ==")
    print(f"Starte mit a = {a}, b = {b}")

    # Exception Check
    if a == 0 and b == 0:
        print("GGT(0, 0) ist nicht definiert. Ich gebe 0 zurück.")
        return 0
    if b == 0:
        print(f"b ist 0, also ist der GGT |a| = {a}")
        return a

    # MainLoop
    while b != 0:
        q = a // b
        r = a % b
        print(f"{a} = {b} * ({q}) + {r}")
        a, b = b, r

    print(f"Fertig! GGT = {a}\n")
    return a


# MAIN
if __name__ == "__main__":
    print("Gib zwei ganze Zahlen ein, ich berechne den GGT.")
    try:
        a = int(input("a = "))
        b = int(input("b = "))
    except ValueError:
        print("Bitte nur ganze Zahlen eingeben!")
    else:
        g = gcd(a, b)
        print(f"GGT({a}, {b}) = {g}")