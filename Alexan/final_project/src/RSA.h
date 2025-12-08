#ifndef RSA_H
#define RSA_H

#include "Cipher.h"
#include <gmpxx.h>
#include <string>

class RSA : public Cipher {
public:
    RSA(const std::string& publicKeyFile = "rsa_key.pub",
        const std::string& privateKeyFile = "rsa_key",
        const mpz_class& minPrime = 1000,
        const mpz_class& maxPrime = 10000);

    void generateKeys(const mpz_class& minPrime, const mpz_class& maxPrime);
    void saveKeys();
    bool loadKeys();

    mpz_class attack(const std::string& cipherFilePath,
                     const std::string& targetPubKeyPath);
    mpz_class decrypt(const mpz_class& cipherText);
    mpz_class encrypt(const mpz_class& clearText);
    void run(
        const std::string& operation,
        const std::string& filePath,
        const mpz_class& pubKey) override;

private:
    std::string publicKeyFile;
    std::string privateKeyFile;
    
    mpz_class n;  // Modulus (public)
    mpz_class e;  // Encryption exponent (public)
    mpz_class d;  // Decryption exponent (private)

    /*** DO NOT STORE p, q, and phi_n ***/
    // These are security risks, if kept around after key generation.

    mpz_class pollardsRho(const mpz_class& n);
    std::pair<mpz_class, mpz_class> readKeyFile(const std::string& filePath);
    bool saveKeyFile(const std::string& filePath, const mpz_class& x) const;
};

#endif