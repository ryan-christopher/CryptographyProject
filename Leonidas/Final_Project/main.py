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

VALID_OPERATIONS = ["generate", "encrypt", "decrypt", "attack"]
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
    Asks the user for a choice until a valid option is selected.
    """
    options_lower = [opt.lower() for opt in options]
    while True:
        choice = lower_string(input(prompt).strip())
        if validate_string_choice(choice, options_lower):
            return choice
        print(color_string(
            f"Invalid input. Allowed options are: {join_strings(options_lower, ', ')}",
            True
        ))


def ask_int(prompt):
    """
    Asks the user for an integer and repeats the input on errors.
    """
    while True:
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            print(color_string("Please enter a valid integer.", True))


def create_cipher(algorithm, operation):
    """
    Creates a cipher object (RSA or ElGamal).
    For 'generate', it asks for the min/max prime range.
    Note: key files are no longer used as input; numeric key components
    are requested interactively in `main` for other operations.
    """
    if operation == "generate":
        min_prime = ask_int("Minimum prime (e.g., 1000): ")
        max_prime = ask_int("Maximum prime (e.g., 10000): ")
        
        if algorithm == "elgamal":
            return ElGamal(min_random_number=min_prime, max_random_number=max_prime)
        else:
            return RSA(min_prime=min_prime, max_prime=max_prime)
    # For non-generate operations we construct ciphers from numeric
    # components directly in `main` (no file IO here).


def handle_rsa(cipher: RSA, operation: str):
    """
    Interactive handling for RSA.
    """
    if operation == "generate":
        print("\n--- RSA Key Generation ---")
        print("Keys are being generated and saved...")
        print(f"\nModulus n = {cipher.n}")
        print(f"Public Exponent e = {cipher.e}")
        print(f"Private Exponent d = {cipher.d}")
        print("\nKeys successfully saved!")
    elif operation == "encrypt":
        print("\n--- RSA Encryption ---")
        print(f"Modulus n = {cipher.n}")
        clear_n = ask_int("Enter the plaintext number (Integer, 0 < m < n): ")
        if clear_n <= 0 or clear_n >= cipher.n:
            raise ValueError(f"Plaintext must be in the range 1..{cipher.n - 1}.")
        cipher_n = cipher.encrypt(clear_n)
        print("\nEncrypted text (as a number):")
        print(cipher_n)

    elif operation == "decrypt":
        print("\n--- RSA Decryption ---")
        cipher_n = ask_int("Enter the ciphertext number: ")
        clear_n = cipher.decrypt(cipher_n)
        print("\nDecrypted text (as a number):")
        print(clear_n)

    elif operation == "attack":
        print("\n--- RSA Attack (Factorization) ---")
        cipher_n = ask_int("Enter the ciphertext number (Integer): ")
        print("Provide target public key components (no key files).")
        n_target = ask_int("Enter target public modulus n: ")
        e_target = ask_int("Enter target public exponent e: ")
        # Use attack_from_components which works with numeric components
        plain = cipher.attack_from_components(cipher_n, n_target, e_target)
        print("\nDetermined plaintext (as a number):")
        print(plain)
    else:
        raise ValueError("Unknown operation for RSA.")


def handle_elgamal(cipher: ElGamal, operation: str):
    """
    Interactive handling for ElGamal.
    """
    if operation == "generate":
        print("\n--- ElGamal Key Generation ---")
        print("Keys are being generated and saved...")
        print(f"\nPrime p = {cipher.p}")
        print(f"Generator g = {cipher.g}")
        print(f"Public Key = {cipher.public_key}")
        print(f"Private Key = {cipher.private_key}")
        print("\nKeys successfully saved!")
    elif operation == "encrypt":
        print("\n--- ElGamal Encryption ---")
        print(f"Prime p = {cipher.p}")
        clear_n = ask_int(f"Enter the plaintext number (Integer, 1..{cipher.p - 1}): ")
        c1, c2 = cipher.encrypt(clear_n)
        print("\nEncrypted text (pair (c1, c2)):")
        print(f"c1 = {c1}")
        print(f"c2 = {c2}")

    elif operation == "decrypt":
        print("\n--- ElGamal Decryption ---")
        c1 = ask_int("Enter c1: ")
        c2 = ask_int("Enter c2: ")
        clear_n = cipher.decrypt((c1, c2))
        print("\nDecrypted text (as a number):")
        print(clear_n)

    elif operation == "attack":
        print("\n--- ElGamal Attack (Discrete Logarithm) ---")
        c1 = ask_int("Enter c1: ")
        c2 = ask_int("Enter c2: ")
        plain = cipher.attack_from_values(c1, c2)
        print("\nDetermined plaintext (as a number):")
        print(plain)
    else:
        raise ValueError("Unknown operation for ElGamal.")


def main():
    print("Small Cryptography Project (RSA / ElGamal) in Python.\n")
    print("You will now be guided step by step through the selection.")
    print(f"Available algorithms: {VALID_ALGOS}")
    print(f"Available operations: {VALID_OPS}\n")

    algorithm = ask_choice("Which algorithm would you like to use? (rsa / elgamal): ",
                           VALID_ALGORITHMS)
    operation = ask_choice("Which operation? (generate / encrypt / decrypt / attack): ",
                           VALID_OPERATIONS)

    try:
        if operation == "generate":
            cipher = create_cipher(algorithm, operation)
            if algorithm == "rsa":
                handle_rsa(cipher, operation)
            else:
                handle_elgamal(cipher, operation)
        else:
            # For non-generate operations we ask for numeric key components
            if algorithm == "rsa":
                if operation == "encrypt":
                    print("Provide public key components (no key files).")
                    n = ask_int("Enter public modulus n: ")
                    e = ask_int("Enter public exponent e: ")
                    cipher = RSA(n=n, e=e)
                    handle_rsa(cipher, operation)

                elif operation == "decrypt":
                    print("Provide private key components (no key files).")
                    n = ask_int("Enter modulus n: ")
                    d = ask_int("Enter private exponent d: ")
                    cipher = RSA(n=n, d=d)
                    handle_rsa(cipher, operation)

                elif operation == "attack":
                    print("RSA attack: provide the ciphertext and the target public key components.")
                    cipher_n = ask_int("Enter the ciphertext number (Integer): ")
                    n_target = ask_int("Enter target public modulus n: ")
                    e_target = ask_int("Enter target public exponent e: ")
                    # Use a small RSA instance to call the attack routine without touching files
                    tmp = RSA(n=1, e=1, d=1)
                    plain = tmp.attack_from_components(cipher_n, n_target, e_target)
                    print("\nDetermined plaintext (as a number):")
                    print(plain)
                else:
                    raise ValueError("Unknown RSA operation")

            else:  # elgamal
                if operation == "encrypt":
                    print("Provide public ElGamal components (no key files).")
                    p = ask_int("Enter prime p: ")
                    g = ask_int("Enter generator g: ")
                    public_key = ask_int("Enter public key (g^x mod p): ")
                    cipher = ElGamal(p=p, g=g, public_key=public_key)
                    handle_elgamal(cipher, operation)

                elif operation == "decrypt":
                    print("Provide private ElGamal components (no key files).")
                    p = ask_int("Enter prime p: ")
                    private_key = ask_int("Enter private key x: ")
                    cipher = ElGamal(p=p, private_key=private_key)
                    handle_elgamal(cipher, operation)

                elif operation == "attack":
                    print("ElGamal attack: provide public components and ciphertext.")
                    p = ask_int("Enter prime p: ")
                    g = ask_int("Enter generator g: ")
                    public_key = ask_int("Enter public key (g^x mod p): ")
                    cipher = ElGamal(p=p, g=g, public_key=public_key)
                    # ask for ciphertext
                    c1 = ask_int("Enter c1: ")
                    c2 = ask_int("Enter c2: ")
                    plain = cipher.attack_from_values(c1, c2)
                    print("\nDetermined plaintext (as a number):")
                    print(plain)
                else:
                    raise ValueError("Unknown ElGamal operation")
    except Exception as err:
        print_and_exit(str(err), code=1)


if __name__ == "__main__":
    main()
