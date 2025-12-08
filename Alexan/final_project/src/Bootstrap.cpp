#include "Bootstrap.h"
#include "crypto_utils.h"

const int INIT_NOT_PRIME = 15;
const int ROUNDS = 20;

Bootstrap::Bootstrap() {
    std::random_device rd;
    rng.seed(rd());
}

mpz_class Bootstrap::randomNumber(size_t bitLength)
{
    mpz_class result = 0;
    size_t bytesNeeded = (bitLength + 7) / 8;
    
    for (size_t i = 0; i < bytesNeeded; i++) {
        uint8_t randomByte = static_cast<uint8_t>(rng() & 0xFF);
        mpz_class byteValue = randomByte;
        byteValue = byteValue << (8 * i);
        result += byteValue;
    }
    
    // Mask to exact bit length
    mpz_class mask = (mpz_class(1) << bitLength) - 1;
    result &= mask;  // Keep only the lower 256 bits
    
    return result;
}

mpz_class Bootstrap::randomOddNumber(size_t bitLength)
{
    mpz_class number = randomNumber(bitLength);
    
    // Set high bit to guarantee a number with bitLength bits.
    mpz_setbit(number.get_mpz_t(), bitLength - 1);
    
    if (number % 2 == 0) {
        number += 1;  // Make it odd.
    }
    
    return number;
}

mpz_class Bootstrap::randomInRange(const mpz_class& min, const mpz_class& max)
{
    mpz_class range = max - min + 1;
    size_t bits_needed = mpz_sizeinbase(range.get_mpz_t(), 2);
    
    mpz_class result = range;  // Initialize to invalid value
    
    while (result >= range) {
        result = randomNumber(bits_needed);
    }
    
    return min + result;
}

mpz_class Bootstrap::generateSeed(const mpz_class& n)
{
    mpz_class seed = randomInRange(2, n - 1);

    while (!areRelativelyPrime(n, seed)) {
        seed = randomInRange(2, n - 1);
    }

    return seed;
}

mpz_class Bootstrap::generatePrimeCongruent3Mod4(size_t bitLength)
{
    mpz_class candidate = INIT_NOT_PRIME;  // Thus starting our while loop.
    
    while (!millerRabinTest(candidate, ROUNDS, *this)) {
        candidate = randomOddNumber(bitLength);
        
        // Ensure it's ≡ 3 (mod 4)
        // Odd numbers are either ≡ 1 (mod 4) or ≡ 3 (mod 4)
        if (candidate % 4 != 3) {
            candidate += 2;  // Change from ≡ 1 to ≡ 3 (mod 4)
        }
    }
        
    return candidate;
}

mpz_class Bootstrap::generatePrimeInRange(const mpz_class& min, const mpz_class& max)
{
    mpz_class candidate = INIT_NOT_PRIME;
    
    while (!millerRabinTest(candidate, ROUNDS, *this)) {
        candidate = randomInRange(min, max);
        
        // Make it odd (all primes except 2 are odd)
        if (candidate % 2 == 0) {
            candidate += 1;
        }
    }
    
    return candidate;
}

mpz_class Bootstrap::generatePrimeInRangeCongruent3Mod4(const mpz_class& min, const mpz_class& max)
{
    mpz_class candidate = INIT_NOT_PRIME;
    
    while (!millerRabinTest(candidate, ROUNDS, *this)) {
        candidate = randomInRange(min, max);
        
        if (candidate % 2 == 0) {
            candidate += 1;  // Make it odd.
        }
        
        // Ensure it's ≡ 3 (mod 4)
        if (candidate % 4 != 3) {
            candidate += 2;  // Change from ≡ 1 to ≡ 3 (mod 4)
        }
    }
    
    return candidate;
}