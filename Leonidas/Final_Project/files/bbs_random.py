# crypto_project/bbs_random.py

from .bootstrap import Bootstrap
from .crypto_utils import mod_pow


class BBSRandom:
    """
    Blum-Blum-Shub random number generator.
    
    """

    def __init__(self, bit_length=512, min_value=None, max_value=None):
        self.n = None
        self.current_s = None
        self.bit_length = None

        bootstrap = Bootstrap()

        if min_value is None or max_value is None:
            # Constructor with bit_length
            self.bit_length = bit_length
            p = bootstrap.generate_prime_congruent_3_mod_4(bit_length)
            q = bootstrap.generate_prime_congruent_3_mod_4(bit_length)
            while p == q:
                q = bootstrap.generate_prime_congruent_3_mod_4(bit_length)
            self.n = p * q
            self.current_s = bootstrap.generate_seed(self.n)
        else:
            # Constructor with [min, max]
            p = bootstrap.generate_prime_in_range_congruent_3_mod_4(min_value, max_value)
            q = bootstrap.generate_prime_in_range_congruent_3_mod_4(min_value, max_value)
            while p == q:
                q = bootstrap.generate_prime_in_range_congruent_3_mod_4(min_value, max_value)
            self.n = p * q
            self.current_s = bootstrap.generate_seed(self.n)

            temp = self.n
            bits_in_n = 0
            while temp > 0:
                bits_in_n += 1
                temp >>= 1
            self.bit_length = bits_in_n

        if self.bit_length is None:
            # Fallback, falls irgendwas schief ging
            self.bit_length = 512

    def rand(self):
        """
        Generates a random number with approximately bit_length bits.
        """
        rand_number = 0
        for x in range(self.bit_length):
            self.current_s = (self.current_s * self.current_s) % self.n
            if self.current_s % 2 == 1:
                rand_number |= (1 << x)
        return rand_number
