/*
My implementation of BBS (Blum Blum Shub) algorithm, to generate
(pseudo) random numbers for generating public-private key pairs
for encryption ciphers such as RSA and El Gamal.
*/
#ifndef BBSRANDOM_H
#define BBSRANDOM_H

#include <gmpxx.h>
#include <utility>
#include <vector>

class BBSRandom {
public:
    BBSRandom(size_t bit_length=512);
    BBSRandom(const mpz_class& min, const mpz_class& max);
    ~BBSRandom();
    mpz_class rand();

private:
    mpz_class n;
    mpz_class current_s;  // Starts as seed, but evolves with each call to rand().
    size_t bitLength;
};

#endif