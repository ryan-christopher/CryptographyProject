#ifndef CRYPTO_UTILS_H
#define CRYPTO_UTILS_H

#include "Bootstrap.h"
#include <gmpxx.h>
#include <set>

// Return true if x and y are relatively prime.  Otherwise, return false.
bool areRelativelyPrime(const mpz_class& x, const mpz_class& y);

// Extended GCD (returns gcd and coefficients x, y such that ax + by = gcd)
mpz_class extendedGCD(const mpz_class& m,
                      const mpz_class& n,
                      mpz_class& x,
                      mpz_class& y
);

// Finds the GCD, using the Euclidean algorithm.
mpz_class findGCD(mpz_class largeNumber, mpz_class smallNumber);

// Returns true if number is prime.  Otherwise, return false.
bool isPrime(const mpz_class& number);

// It's probabaly prime....or not.  :)
bool millerRabinTest(const mpz_class& n, int rounds, Bootstrap& rng);

// Compute modular inverse: a^(-1) mod m
mpz_class modInverse(const mpz_class& a, const mpz_class& m);

// Computes base^exp % mod using fast modular exponentiation
mpz_class modPow(mpz_class base, mpz_class exp, const mpz_class& mod);

// Finds and returns a generator (i.e., primitive root) modulo prime p
mpz_class findGenerator(const mpz_class& p);

// Returns the set of unique prime factors of n
std::set<mpz_class> getPrimeFactors(mpz_class n);

// Checks if g is a primitive root modulo p using the given
// prime factors of (p-1)
bool isPrimitiveRoot(const mpz_class& g,
                     const mpz_class& p,
                     const std::set<mpz_class>& primeFactors);

#endif