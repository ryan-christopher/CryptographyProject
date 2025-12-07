# crypto_project/bootstrap.py

import random
from .crypto_utils import are_relatively_prime, miller_rabin_test


INIT_NOT_PRIME = 15
ROUNDS = 20


class Bootstrap:
    """
    Entspricht grob deiner C++-Klasse Bootstrap.
    Nutzt Pythons random, um Startwerte und Kandidaten zu erzeugen.
    """

    def __init__(self):
        # SystemRandom nutzt OS-Randomness
        self.rng = random.SystemRandom()

    def random_number(self, bit_length):
        if bit_length <= 0:
            raise ValueError("bit_length muss > 0 sein")

        result = 0
        bytes_needed = (bit_length + 7) // 8

        for _ in range(bytes_needed):
            random_byte = self.rng.randrange(0, 256)
            result = (result << 8) | random_byte

        # Maske auf gewünschte Bitlänge
        mask = (1 << bit_length) - 1
        result = result & mask

        # Höchstes Bit setzen, damit es wirklich bit_length Bits sind
        result |= (1 << (bit_length - 1))

        return result

    def random_odd_number(self, bit_length):
        number = self.random_number(bit_length)
        if number % 2 == 0:
            number += 1
        return number

    def random_in_range(self, min_value, max_value):
        if min_value > max_value:
            raise ValueError("min_value darf nicht größer als max_value sein")

        min_value = int(min_value)
        max_value = int(max_value)
        range_val = max_value - min_value + 1
        bits_needed = range_val.bit_length()
        result = range_val

        while result >= range_val:
            candidate = self.random_number(bits_needed)
            result = candidate

        return min_value + result

    def generate_seed(self, n):
        """
        Erzeugt Seed s mit 2 <= s <= n-1 und gcd(s, n) = 1.
        """
        n = int(n)
        seed = self.random_in_range(2, n - 1)
        while not are_relatively_prime(seed, n):
            seed = self.random_in_range(2, n - 1)
        return seed

    def generate_prime_congruent_3_mod_4(self, bit_length):
        """
        Erzeugt eine Primzahl p mit p ≡ 3 (mod 4).
        """
        candidate = INIT_NOT_PRIME
        while not miller_rabin_test(candidate, ROUNDS, self):
            candidate = self.random_odd_number(bit_length)
            if candidate % 4 != 3:
                candidate += 2
        return candidate

    def generate_prime_in_range(self, min_value, max_value):
        """
        Erzeugt eine Primzahl im Bereich [min_value, max_value].
        """
        candidate = INIT_NOT_PRIME
        while not miller_rabin_test(candidate, ROUNDS, self):
            candidate = self.random_in_range(min_value, max_value)
            if candidate % 2 == 0:
                candidate += 1
        return candidate

    def generate_prime_in_range_congruent_3_mod_4(self, min_value, max_value):
        """
        Erzeugt eine Primzahl im Bereich [min, max] mit p ≡ 3 (mod 4).
        """
        candidate = INIT_NOT_PRIME
        while not miller_rabin_test(candidate, ROUNDS, self):
            candidate = self.random_in_range(min_value, max_value)
            if candidate % 2 == 0:
                candidate += 1
            if candidate % 4 != 3:
                candidate += 2
        return candidate
