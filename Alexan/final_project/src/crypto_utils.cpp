#include "crypto_utils.h"

bool areRelativelyPrime(const mpz_class& x, const mpz_class& y)
{
    mpz_class gcd = (x > y) ? findGCD(x, y) : findGCD(y, x);
    return gcd == 1;
}

mpz_class extendedGCD(const mpz_class& m, const mpz_class& n, mpz_class& x, mpz_class& y)
{
    mpz_class old_r = m, r = n;
    mpz_class old_s = 1, s = 0;
    mpz_class old_t = 0, t = 1;

    while (r != 0) {
        mpz_class quotient = old_r / r;

        // Update remainders
        // (old_r, r) = (r, old_r - quotient * r)
        mpz_class temp_r = r;
        r = old_r - quotient * r;
        old_r = temp_r;

        // Update s-coefficients (for x)
        // (old_s, s) = (s, old_s - quotient * s)
        mpz_class temp_s = s;
        s = old_s - quotient * s;
        old_s = temp_s;

        // Update t-coefficients (for y)
        // (old_t, t) = (t, old_t - quotient * t)
        mpz_class temp_t = t;
        t = old_t - quotient * t;
        old_t = temp_t;
    }

    // When r = 0, the GCD is old_r.
    // The coefficients are old_s and old_t.
    x = old_s;
    y = old_t;
    
    return old_r; // This is the GCD
}

mpz_class findGCD(mpz_class largeNumber, mpz_class smallNumber)
{
    // My implementation of Euclidean algorithm.
    mpz_class remainder = largeNumber % smallNumber;

    while (remainder > 0) {
        largeNumber = smallNumber;
        smallNumber = remainder;
        remainder = largeNumber % smallNumber;
    }

    return smallNumber;
}

bool isPrime(const mpz_class& number)
{
    if (number <= 1) return false;
    if (number <= 3) return true;
    if (number % 2 == 0 || number % 3 == 0) return false;
    
    for (int i = 5; i * i <= number; i += 6) {
        if (number % i == 0 || number % (i + 2) == 0)
            return false;
    }

    return true;
}

bool millerRabinTest(const mpz_class& n, int rounds, Bootstrap& rng) 
{
    if (n <= 1) return false;
    if (n <= 3) return true;
    if (n % 2 == 0) return false;

    // Write n-1 as 2^r × m
    mpz_class m = n - 1;
    size_t r = 0;
    
    while (m % 2 == 0) {
        m = m / 2;
        r++;
    }

    const int k = rounds;

    for (int i = 0; i < k; i++) {
        mpz_class b = rng.randomInRange(2, n - 2);
        
        // Compute b^m mod n using modular exponentiation
        mpz_class x;
        mpz_powm(x.get_mpz_t(), b.get_mpz_t(), m.get_mpz_t(), n.get_mpz_t());

        /* mpz_powm() function is like my modpow() function
          (seen in lecture4/bsgs.cpp) but optimized to work
          with mpz_class numbers.
        */
        // If b^m ≡ 1 or -1 (mod n), continue to next base
        if (x == 1 || x == n - 1) {
            continue;
        }
        
        // Square repeatedly r-1 times
        bool foundMinusOne = false;
        for (size_t j = 0; j < r - 1; j++) {
            mpz_powm_ui(x.get_mpz_t(), x.get_mpz_t(), 2, n.get_mpz_t());
            
            if (x == n - 1) {
                foundMinusOne = true;
                break;
            }
        }
        
        if (!foundMinusOne) {
            return false;  // n is comosite, not prime.
        }
    }

    return true;
}

mpz_class modInverse(const mpz_class& a, const mpz_class& m)
{
    mpz_class x, y;
    mpz_class gcd = extendedGCD(a, m , x, y);

    if (gcd != 1) {
        throw std::runtime_error("Modular inverse does not exist (gcd != 1)");
    }

    mpz_class result = x % m;

    if (result < 0) {
        result += m;
    }

    return result;
}

mpz_class modPow(mpz_class base, mpz_class exp, const mpz_class& mod)
{
    mpz_class result = 1;
    
    base %= mod;

    while (exp > 0) {
        if (exp % 2 == 1) {
            result = (result * base) % mod;
        }

        base = (base * base) % mod;
        exp /= 2;
    }

    return result;
}

mpz_class findGenerator(const mpz_class& p)
{
    std::set<mpz_class> q = getPrimeFactors(p - 1);

    for (mpz_class b = 2; b < p; b++) {
        if (isPrimitiveRoot(b, p, q)) {
            return b;
        }
    }

    throw std::runtime_error("Could not find generator");
}

std::set<mpz_class> getPrimeFactors(mpz_class n)
{
    std::set<mpz_class> primeFactors;

    // Factor out even numbers
    if (n % 2 == 0) {
        primeFactors.insert(2);

        while (n % 2 == 0) {
            n /= 2;
        }
    }

    // Factor out odd numbers
    for (mpz_class i = 3; i * i <= n; i += 2) {
        if (n % i == 0) {
            primeFactors.insert(i);

            while (n % i == 0) {
                n /= i;
            }
        }
    }

    // Remaining n is a prime factor.
    if (n > 1) {
        primeFactors.insert(n);
    }

    return primeFactors;
}

bool isPrimitiveRoot(const mpz_class& b,
                     const mpz_class& p,
                     const std::set<mpz_class>& q)
{
    for (mpz_class primeFactor : q) {
        mpz_class x = modPow(b, (p - 1) / primeFactor, p);

        if (x == 1) {
            return false;
        }
    }

    return true;
}