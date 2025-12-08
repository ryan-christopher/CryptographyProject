/*
The Bootstrap class uses C++'s built-in random number generator to generate the
initial prime numbers and seed needed to initialize the cryptographically-secure
BBSRandom generator, after which it's never used again.
*/
#ifndef BOOTSTRAP_H
#define BOOTSTRAP_H

#include <gmpxx.h>
#include <random>

class Bootstrap {
public:
    Bootstrap();

    mpz_class randomNumber(size_t bitLength);
    mpz_class randomOddNumber(size_t bitLength);
    mpz_class randomInRange(const mpz_class& min, const mpz_class& max);

    mpz_class generateSeed(const mpz_class& n);
    mpz_class generatePrimeCongruent3Mod4(size_t bitLength);
    mpz_class generatePrimeInRange(const mpz_class& min, const mpz_class& max);
    mpz_class generatePrimeInRangeCongruent3Mod4(const mpz_class& min, const mpz_class& max);

private:
    std::mt19937_64 rng;
};

#endif