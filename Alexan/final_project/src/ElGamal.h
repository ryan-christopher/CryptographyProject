#ifndef ELGAMAL_H
#define ELGAMAL_H
#include "Cipher.h"
#include <gmpxx.h>
#include <utility>

class ElGamal : public Cipher {
public:
    ElGamal(const std::string& publicKeyFile = "elgamal_key.pub",
            const std::string& privateKeyFile = "elgamal_key",
            const mpz_class& minRandomNumber = 1000,
            const mpz_class& maxRandomNumber = 10000);

    void generateKeys(const mpz_class& min, const mpz_class& max);
    void saveKeys();
    bool loadKeys();

    mpz_class attack(const std::string& cipherFilePath);
    mpz_class decrypt(const std::pair<mpz_class, mpz_class>& cipherText);
    std::pair<mpz_class, mpz_class> encrypt(const mpz_class& clearText, 
                                            const mpz_class& pubKey);
    void run(
        const std::string& operation,
        const std::string& filePath,
        const mpz_class& pubKey) override;

private:
    mpz_class p;  // Our large prime
    mpz_class g;  // Our generator for p
    mpz_class publicKey;
    mpz_class privateKey;
    std::string publicKeyFile;
    std::string privateKeyFile;

    mpz_class babyStepGiantStep(
        const mpz_class& a,
        const mpz_class& g,
        const mpz_class& p
    );
};

#endif