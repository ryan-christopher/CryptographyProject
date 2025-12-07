# crypto_project/elgamal_cipher.py

import sys
from .cipher_base import CipherBase
from .bootstrap import Bootstrap
from .crypto_utils import (
    mod_pow,
    mod_inverse,
    find_generator,
)
from .string_utils import color_string


class ElGamal(CipherBase):
    """
    ElGamal implementation in Python.
    """

    def __init__(
        self,
        public_key_file="elgamal_key.pub",
        private_key_file="elgamal_key",
        min_random_number=1,
        max_random_number=10000,
        load_from_files=True,
        p: int = None,
        g: int = None,
        public_key: int = None,
        private_key: int = None,
    ):
        self.public_key_file = public_key_file
        self.private_key_file = private_key_file

        self.p = None
        self.g = None
        self.public_key = None
        self.private_key = None

        # If numeric components provided, use them directly
        if p is not None:
            self.p = int(p)
            self.g = int(g) if g is not None else None
            self.public_key = int(public_key) if public_key is not None else None
            self.private_key = int(private_key) if private_key is not None else None
            return

        if load_from_files and self.load_keys():
            sys.stderr.write("Found existing ElGamal keys.\n")
            sys.stderr.write(f"  Public:  {self.public_key_file}\n")
            sys.stderr.write(f"  Private: {self.private_key_file}\n")
        else:
            sys.stderr.write("No existing ElGamal keys found. Generating new keys...\n")
            sys.stderr.write(f"  Prime range: [{min_random_number}, {max_random_number}]\n")
            self.generate_keys(min_random_number, max_random_number)
            try:
                self.save_keys()
            except RuntimeError:
                pass
            sys.stderr.write("Keys generated\n")

    def generate_keys(self, min_value, max_value):
        bootstrap = Bootstrap()
        self.p = bootstrap.generate_prime_in_range(min_value, max_value)
        self.g = find_generator(self.p)
        self.private_key = bootstrap.random_in_range(2, self.p - 2)
        self.public_key = mod_pow(self.g, self.private_key, self.p)

    def load_keys(self):
        # Public key file
        try:
            with open(self.public_key_file, "r", encoding="utf-8") as pub_file:
                lines = pub_file.read().strip().splitlines()
        except OSError:
            return False

        if len(lines) < 3:
            return False

        self.p = int(lines[0].strip())
        self.g = int(lines[1].strip())
        self.public_key = int(lines[2].strip())

        # Private key file
        try:
            with open(self.private_key_file, "r", encoding="utf-8") as priv_file:
                line = priv_file.read().strip()
        except OSError:
            return False

        if not line:
            return False

        self.private_key = int(line)
        return True

    def save_keys(self):
        try:
            with open(self.public_key_file, "w", encoding="utf-8") as pub_file:
                pub_file.write(str(self.p) + "\n")
                pub_file.write(str(self.g) + "\n")
                pub_file.write(str(self.public_key) + "\n")
        except OSError:
            msg = f"Could not create public key file: {self.public_key_file}"
            raise RuntimeError(msg)

        try:
            with open(self.private_key_file, "w", encoding="utf-8") as priv_file:
                priv_file.write(str(self.private_key) + "\n")
        except OSError:
            msg = f"Could not create private key file: {self.private_key_file}"
            raise RuntimeError(msg)

    def baby_step_giant_step(self, a, value, p):
        """
        Solve a^x ≡ value (mod p) via Baby-Step Giant-Step.
        Used to recover the private key from (p, g, publicKey).
        """
        from math import isqrt

        a = int(a)
        value = int(value)
        p = int(p)

        n = p - 1
        m = isqrt(n) + 1

        # Tabelle L1: a^(j*m)
        L1 = {}
        for j in range(m + 1):
            val = mod_pow(a, j * m, p)
            L1[val] = j

        a_inv = mod_inverse(a, p)
        gamma = value

        for i in range(m + 1):
            if gamma in L1:
                j = L1[gamma]
                x = m * j - i

                sys.stderr.write(f"Match found! L2[{i}] = L1[{j}] = {gamma}\n")
                sys.stderr.write(f"i = {i}, j = {j}\n")
                sys.stderr.write(f"Private key x = {x}\n")

                check = mod_pow(a, x, p)
                if check == value:
                    sys.stderr.write(f"Verified: {a}^{x} ≡ {value} (mod {p})\n")
                    return x
                else:
                    sys.stderr.write("Verification failed with m*j - i, trying m*j + i...\n")
                    x_alt = m * j + i
                    check_alt = mod_pow(a, x_alt, p)
                    if check_alt == value:
                        sys.stderr.write(f"Verified: {a}^{x_alt} ≡ {value} (mod {p})\n")
                        return x_alt

            gamma = (gamma * a_inv) % p

        raise RuntimeError("Baby-Step Giant-Step failed to find x")

    def attack(self, cipher_file_path):
        """
        Attack on ElGamal: discrete logarithm via Baby-Step Giant-Step.
        """
        sys.stderr.write("\n=== ElGamal Attack (Discrete Logarithm) ===\n")

        sys.stderr.write("\nStep 1: Recovering private key x from public key (p, g, publicKey)...\n")
        recovered_x = self.baby_step_giant_step(self.g, self.public_key, self.p)
        sys.stderr.write(f"\nSuccessfully recovered private key: x = {recovered_x}\n")

        sys.stderr.write(f"\nStep 2: Reading ciphertext from {cipher_file_path}...\n")
        text = self.read_file(cipher_file_path)
        from io import StringIO
        buffer = StringIO(text)
        line1 = buffer.readline().strip()
        line2 = buffer.readline().strip()

        c1 = int(line1)
        c2 = int(line2)

        sys.stderr.write(f"Ciphertext: ({c1}, {c2})\n")
        sys.stderr.write("\nStep 3: Decrypting using recovered private key...\n")

        original_x = self.private_key
        self.private_key = recovered_x
        plaintext = self.decrypt((c1, c2))
        self.private_key = original_x

        msg = color_string(str(plaintext))
        sys.stderr.write("\nSuccessfully decrypted message: " + msg + "\n")

        return plaintext

    def attack_from_values(self, c1, c2):
        """
        Attack like in attack(), but (c1, c2) are directly provided as values
        instead of being read from a file.
        """
        sys.stderr.write("\n=== ElGamal Attack (Discrete Logarithm) ===\n")

        sys.stderr.write("\nStep 1: Recovering private key x from public key (p, g, publicKey)...\n")
        recovered_x = self.baby_step_giant_step(self.g, self.public_key, self.p)
        sys.stderr.write(f"\n Successfully recovered private key: x = {recovered_x}\n")

        sys.stderr.write("\nStep 2: Decrypting given ciphertext (c1, c2)...\n")
        c1 = int(c1)
        c2 = int(c2)
        original_x = self.private_key
        self.private_key = recovered_x
        plaintext = self.decrypt((c1, c2))
        self.private_key = original_x

        msg = color_string(str(plaintext))
        sys.stderr.write("\n Successfully decrypted message: " + msg + "\n")

        return plaintext

    def decrypt(self, cipher_pair):
        c1, c2 = cipher_pair
        s = mod_pow(c1, self.private_key, self.p)
        s_inv = mod_inverse(s, self.p)
        clear_text = (c2 * s_inv) % self.p
        return clear_text

    def encrypt(self, clear_text):
        clear_text = int(clear_text)
        if clear_text <= 0 or clear_text >= self.p:
            raise ValueError("ERROR: Message must be in range [1, p-1]")

        bootstrap = Bootstrap()
        k = bootstrap.random_in_range(2, self.p - 2)
        c1 = mod_pow(self.g, k, self.p)
        c2 = (clear_text * mod_pow(self.public_key, k, self.p)) % self.p
        return c1, c2

    def run(self, operation, file_path):
        self.print_run_header("El Gamal", operation, file_path)

        operation = operation.lower()
        if operation == "attack":
            result = self.attack(file_path)
            print(result)
            return

        text_type = "cipher" if operation == "decrypt" else "clear"
        sys.stderr.write(f"Reading {text_type}-text file: {file_path} ... ")
        text = self.read_file(file_path)
        sys.stderr.write("Done!\n")
        sys.stderr.write(operation + "ing ... ")

        output = ""

        if operation == "encrypt":
            clear_text = int(text.strip())
            c1, c2 = self.encrypt(clear_text)
            output = str(c1) + "\n" + str(c2)
        else:
            lines = text.strip().splitlines()
            if len(lines) < 2:
                raise RuntimeError("Ciphertext for ElGamal must have two lines (c1 und c2)")
            c1 = int(lines[0].strip())
            c2 = int(lines[1].strip())
            clear_text = self.decrypt((c1, c2))
            output = str(clear_text)

        sys.stderr.write("Done!\n")
        print(output)
