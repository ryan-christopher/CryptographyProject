#include "BBSRandom.h"
#include "Bootstrap.h"
#include "crypto_utils.h"

BBSRandom::BBSRandom(size_t bit_length)
{
    bitLength = bit_length;

    Bootstrap b;
    const mpz_class p = b.generatePrimeCongruent3Mod4(bitLength);
    mpz_class q = b.generatePrimeCongruent3Mod4(bitLength);

    while (p == q) {
        q = b.generatePrimeCongruent3Mod4(bitLength);
    }

    n = p * q;
    current_s = b.generateSeed(n);
}

BBSRandom::BBSRandom(const mpz_class& min, const mpz_class& max)
{
    Bootstrap b;
    const mpz_class p = b.generatePrimeInRangeCongruent3Mod4(min, max);    
    mpz_class q = b.generatePrimeInRangeCongruent3Mod4(min, max);

    while (p == q) {
        q = b.generatePrimeInRangeCongruent3Mod4(min, max);
    }
    
    n = p * q;
    current_s = b.generateSeed(n);
    
    // Calculate bitLength from n
    size_t bits_in_n = 0;
    mpz_class temp = n;
    while (temp > 0) {
        bits_in_n++;
        temp = temp >> 1;
    }
    bitLength = bits_in_n;
}

BBSRandom::~BBSRandom() {}

mpz_class BBSRandom::rand()
{
    mpz_class randNumber = 0;

    for (int x = 0; x < bitLength; ++x) {
        current_s = (current_s * current_s) % n;

        if (current_s % 2 == 1) {
            mpz_setbit(randNumber.get_mpz_t(), x);
        }
    }

    return randNumber;
}