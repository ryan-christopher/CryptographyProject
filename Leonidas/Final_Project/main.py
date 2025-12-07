import sys
from files.rsa_cipher import RSA
from files.elgamal_cipher import ElGamal
from files.string_utils import (
    color_string,
    join_strings,
    lower_string,
)


VALID_ALGORITHMS = ["elgamal", "rsa"]
VALID_ALGOS = join_strings(VALID_ALGORITHMS, ", ")

VALID_OPERATIONS = ["attack", "decrypt", "encrypt"]
VALID_OPS = join_strings(VALID_OPERATIONS, ", ")


def print_and_exit(msg, code=0):
    sys.stderr.write(color_string(msg, code == 1) + "\n")
    sys.exit(code)


def validate_string_choice(choice, options):
    for option in options:
        if choice == option:
            return True
    return False


def ask_choice(prompt, options):
    """
    Fragt den User nach einer Auswahl, bis eine gültige Option gewählt wurde.
    """
    options_lower = [opt.lower() for opt in options]
    while True:
        choice = lower_string(input(prompt).strip())
        if validate_string_choice(choice, options_lower):
            return choice
        print(color_string(
            f"Ungültige Eingabe. Erlaubt sind: {join_strings(options_lower, ', ')}",
            True
        ))


def ask_int(prompt):
    """
    Fragt den User nach einem Integer und wiederholt die Eingabe bei Fehlern.
    """
    while True:
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            print(color_string("Bitte gib eine gültige Ganzzahl ein.", True))


def create_cipher(algorithm):
    """
    Erstellt ein Cipher-Objekt (RSA oder ElGamal) und fragt optional
    einen Key-Datei-Basisnamen ab.
    """
    key_basename = input(
        "Optional: Basisname für Key-Dateien (Enter für Standard, "
        "z.B. 'rsa_key' / 'elgamal_key'): "
    ).strip()

    if key_basename:
        if algorithm == "elgamal":
            return ElGamal(public_key_file=key_basename + ".pub",
                           private_key_file=key_basename)
        else:
            return RSA(public_key_file=key_basename + ".pub",
                       private_key_file=key_basename)
    else:
        # Standard-Keys nutzen
        if algorithm == "elgamal":
            return ElGamal()
        else:
            return RSA()


def handle_rsa(cipher: RSA, operation: str):
    """
    Interaktive Bedienung für RSA.
    """
    if operation == "encrypt":
        print("\n--- RSA Verschlüsselung ---")
        print(f"Modulus n = {cipher.n}")
        clear_n = ask_int("Gib die Klartextzahl ein (Integer, 0 < m < n): ")
        if clear_n <= 0 or clear_n >= cipher.n:
            raise ValueError(f"Klartext muss im Bereich 1..{cipher.n - 1} liegen.")
        cipher_n = cipher.encrypt(clear_n)
        print("\nVerschlüsselter Text (als Zahl):")
        print(cipher_n)

    elif operation == "decrypt":
        print("\n--- RSA Entschlüsselung ---")
        cipher_n = ask_int("Gib die Chiffretextzahl ein: ")
        clear_n = cipher.decrypt(cipher_n)
        print("\nEntschlüsselter Text (als Zahl):")
        print(clear_n)

    elif operation == "attack":
        print("\n--- RSA Angriff (Faktorisierung) ---")
        cipher_n = ask_int("Gib den Chiffretext ein (Integer): ")
        pubkey_path = input(
            "Pfad zur öffentlichen Schlüsseldatei des Ziels "
            "(Default: target_rsa_key.pub): "
        ).strip()
        if not pubkey_path:
            pubkey_path = "target_rsa_key.pub"
        plain = cipher.attack_from_value(cipher_n, pubkey_path)
        print("\nErmittelter Klartext (als Zahl):")
        print(plain)
    else:
        raise ValueError("Unbekannte Operation für RSA.")


def handle_elgamal(cipher: ElGamal, operation: str):
    """
    Interaktive Bedienung für ElGamal.
    """
    if operation == "encrypt":
        print("\n--- ElGamal Verschlüsselung ---")
        print(f"Primzahl p = {cipher.p}")
        clear_n = ask_int(f"Gib die Klartextzahl ein (Integer, 1..{cipher.p - 1}): ")
        c1, c2 = cipher.encrypt(clear_n)
        print("\nVerschlüsselter Text (Paar (c1, c2)):")
        print(f"c1 = {c1}")
        print(f"c2 = {c2}")

    elif operation == "decrypt":
        print("\n--- ElGamal Entschlüsselung ---")
        c1 = ask_int("Gib c1 ein: ")
        c2 = ask_int("Gib c2 ein: ")
        clear_n = cipher.decrypt((c1, c2))
        print("\nEntschlüsselter Text (als Zahl):")
        print(clear_n)

    elif operation == "attack":
        print("\n--- ElGamal Angriff (Diskreter Logarithmus) ---")
        c1 = ask_int("Gib c1 ein: ")
        c2 = ask_int("Gib c2 ein: ")
        plain = cipher.attack_from_values(c1, c2)
        print("\nErmittelter Klartext (als Zahl):")
        print(plain)
    else:
        raise ValueError("Unbekannte Operation für ElGamal.")


def main():
    print("Kleines Kryptographie-Projekt (RSA / ElGamal) in Python.\n")
    print("Du wirst nun schrittweise durch die Auswahl geführt.")
    print(f"Verfügbare Algorithmen: {VALID_ALGOS}")
    print(f"Verfügbare Operationen: {VALID_OPS}\n")

    algorithm = ask_choice("Welchen Algorithmus möchtest du nutzen? (rsa / elgamal): ",
                           VALID_ALGORITHMS)
    operation = ask_choice("Welche Operation? (encrypt / decrypt / attack): ",
                           VALID_OPERATIONS)

    try:
        cipher = create_cipher(algorithm)
        if algorithm == "rsa":
            handle_rsa(cipher, operation)
        else:
            handle_elgamal(cipher, operation)
    except Exception as err:
        print_and_exit(str(err), code=1)


if __name__ == "__main__":
    main()
