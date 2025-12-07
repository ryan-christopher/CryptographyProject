# crypto_project/rsa_cipher.py

import sys
from .cipher_base import CipherBase
from .bootstrap import Bootstrap
from .bbs_random import BBSRandom
from .crypto_utils import (
    are_relatively_prime,
    mod_inverse,
    mod_pow,
    find_gcd,
)
from .string_utils import color_string


class RSA(CipherBase):
    """
    RSA class in Python.
    """

    def __init__(
        self,
        public_key_file="rsa_key.pub",
        private_key_file="rsa_key",
        min_prime=1000,
        max_prime=10000,
        load_from_files=True,
        n: int = None,
        e: int = None,
        d: int = None,
    ):
        self.public_key_file = public_key_file
        self.private_key_file = private_key_file

        self.n = None
        self.e = None
        self.d = None

        # If numeric key components were provided directly, use them
        if n is not None:
            self.n = int(n)
            self.e = int(e) if e is not None else None
            self.d = int(d) if d is not None else None
            return

        # Otherwise try to load from files (legacy behaviour) or generate new keys
        if load_from_files and self.load_keys():
            sys.stderr.write("Found existing RSA keys.\n")
            sys.stderr.write(f"  Public:  {self.public_key_file}\n")
            sys.stderr.write(f"  Private: {self.private_key_file}\n")
        else:
            sys.stderr.write("No existing RSA keys found. Generating new keys...\n")
            sys.stderr.write(f"  Prime range: [{min_prime}, {max_prime}]\n")
            self.generate_keys(min_prime, max_prime)
            try:
                self.save_keys()
            except RuntimeError:
                # If saving fails, continue with in-memory keys
                pass
            sys.stderr.write("Keys generated\n")

    def generate_keys(self, min_prime, max_prime):
        bootstrap = Bootstrap()
        sys.stderr.write("Generating prime p...\n")
        p = bootstrap.generate_prime_in_range(min_prime, max_prime)
        sys.stderr.write("Generating prime q...\n")
        q = bootstrap.generate_prime_in_range(min_prime, max_prime)

        while p == q:
            q = bootstrap.generate_prime_in_range(min_prime, max_prime)

        n = p * q
        phi_n = (p - 1) * (q - 1)
        e = 65537

        while not are_relatively_prime(e, phi_n):
            e += 2

        d = mod_inverse(e, phi_n)
        verify = (e * d) % phi_n
        if verify != 1:
            raise RuntimeError("Key generation failed: e*d mod φ(n) != 1")

        self.n = n
        self.e = e
        self.d = d

    def save_key_file(self, file_path, exponent):
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(str(self.n) + "\n")
                f.write(str(exponent) + "\n")
            return True
        except OSError:
            return False

    def save_keys(self):
        if not self.save_key_file(self.public_key_file, self.e):
            msg = f"Could not create public key file: {self.public_key_file}"
            raise RuntimeError(msg)

        if not self.save_key_file(self.private_key_file, self.d):
            msg = f"Could not create private key file: {self.private_key_file}"
            raise RuntimeError(msg)

    def read_key_file(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as key_file:
                lines = key_file.read().strip().splitlines()
        except OSError:
            msg = f"ERROR: Could not open key file: {file_path}"
            raise RuntimeError(msg)

        if len(lines) < 2:
            msg = f"ERROR: Invalid key file (needs 2 Zeilen): {file_path}"
            raise RuntimeError(msg)

        n = int(lines[0].strip())
        e_or_d = int(lines[1].strip())
        return n, e_or_d

    def load_keys(self):
        # Public Key
        try:
            n_pub, e = self.read_key_file(self.public_key_file)
            self.n = n_pub
            self.e = e
        except RuntimeError:
            return False

        # Private Key
        try:
            n_priv, d = self.read_key_file(self.private_key_file)
            if n_priv != self.n:
                raise RuntimeError("Public and private key moduli do not match")
            self.d = d
        except RuntimeError:
            return False

        return True

    def pollards_rho(self, n):
        """
        Factorization of n using Pollard's Rho.
        """
        n = int(n)
        if n == 1:
            return 1
        if n % 2 == 0:
            return 2

        x = 5
        y = 26
        d = 1

        while d == 1:
            x = (x * x + 1) % n
            y = (y * y + 1) % n
            y = (y * y + 1) % n

            diff = x - y
            if diff < 0:
                diff = -diff
            d = find_gcd(diff, n)

            if d == n:
                rng = BBSRandom()
                x = rng.rand() % n
                y = rng.rand() % n
                d = 1

        return d

    def attack(self, cipher_file_path, target_pubkey_path):
        """
        Attack: Factorization of the target modulus and recovery of the plaintext.
        """
        sys.stderr.write("\n=== RSA (Factorization) ===\n\n")

        sys.stderr.write(f"Step 1: Read public key {target_pubkey_path}...\n\n")
        n_target, e_target = self.read_key_file(target_pubkey_path)

        sys.stderr.write("Step 2: Finding divisor of n ...\n\n")
        p = self.pollards_rho(n_target)
        q = n_target // p

        sys.stderr.write(f"Step 3: Calculating phi({n_target}) ...\n\n")
        phi = (p - 1) * (q - 1)

        sys.stderr.write("Step 4: Calculating private exponent d ...\n\n")
        d_target = mod_inverse(e_target, phi)

        sys.stderr.write(f"Step 5: Reading ciphertext from {cipher_file_path}...\n")
        text = self.read_file(cipher_file_path)
        cipher_text = int(text.strip())

        plain_text = mod_pow(cipher_text, d_target, n_target)
        msg = color_string(str(plain_text))
        sys.stderr.write("\n Successfully decrypted message: " + msg + "\n")

        return plain_text
    
    def attack_from_value(self, cipher_text, target_pubkey_path="target_rsa_key.pub"):
        """
        Attack like in attack(), but the ciphertext is directly provided as a number
        instead of being read from a file.
        """
        sys.stderr.write("\n=== RSA (Factorization) ===\n\n")

        sys.stderr.write(f"Step 1: Read public key {target_pubkey_path}...\n\n")
        n_target, e_target = self.read_key_file(target_pubkey_path)

        sys.stderr.write("Step 2: Finding divisor of n ...\n\n")
        p = self.pollards_rho(n_target)
        q = n_target // p

        sys.stderr.write(f"Step 3: Calculating phi({n_target}) ...\n\n")
        phi = (p - 1) * (q - 1)

        sys.stderr.write("Step 4: Calculating private exponent d ...\n\n")
        d_target = mod_inverse(e_target, phi)

        sys.stderr.write("Step 5: Decrypting ciphertext value ...\n")
        cipher_text = int(cipher_text)
        plain_text = mod_pow(cipher_text, d_target, n_target)
        msg = color_string(str(plain_text))
        sys.stderr.write("\n Successfully decrypted message: " + msg + "\n")

        return plain_text

    def attack_from_components(self, cipher_text, n_target, e_target):
        """
        Faktorisiere n_target und entschlüssele cipher_text, wenn die
        öffentlichen Komponenten (n_target, e_target) direkt übergeben werden.
        """
        sys.stderr.write("\n=== RSA (Factorization) ===\n\n")

        sys.stderr.write("Step 2: Finding divisor of n ...\n\n")
        p = self.pollards_rho(n_target)
        q = n_target // p

        sys.stderr.write(f"Step 3: Calculating phi({n_target}) ...\n\n")
        phi = (p - 1) * (q - 1)

        sys.stderr.write("Step 4: Calculating private exponent d ...\n\n")
        d_target = mod_inverse(e_target, phi)

        sys.stderr.write("Step 5: Decrypting ciphertext value ...\n")
        cipher_text = int(cipher_text)
        plain_text = mod_pow(cipher_text, d_target, n_target)
        msg = color_string(str(plain_text))
        sys.stderr.write("\n✅ Successfully decrypted message: " + msg + "\n")

        return plain_text

    def decrypt(self, cipher_text):
        cipher_text = int(cipher_text)
        clear_text = mod_pow(cipher_text, self.d, self.n)
        return clear_text

    def encrypt(self, clear_text):
        clear_text = int(clear_text)
        cipher_text = mod_pow(clear_text, self.e, self.n)
        return cipher_text

    def run(self, operation, file_path):
        self.print_run_header("RSA", operation, file_path)

        operation = operation.lower()

        if operation == "attack":
            target_pub = "target_rsa_key.pub"
            result = self.attack(file_path, target_pub)
            print(result)
            return

        text_type = "cipher" if operation == "decrypt" else "clear"
        sys.stderr.write(f"Reading {text_type}-text file: {file_path} ... ")
        text = self.read_file(file_path)
        sys.stderr.write("Done!\n")
        sys.stderr.write(operation + "ing ... ")

        output = ""

        if operation == "encrypt":
            clear_n = int(text.strip())
            output = str(self.encrypt(clear_n))
        else:
            cipher_n = int(text.strip())
            output = str(self.decrypt(cipher_n))

        sys.stderr.write("Done!\n")
        print(output)
