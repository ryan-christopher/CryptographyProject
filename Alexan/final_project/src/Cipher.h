#ifndef CIPHER_H
#define CIPHER_H
#include <gmpxx.h>
#include <string>

class Cipher {
public:
    virtual void run(
        const std::string& operation,
        const std::string& filePath,
        const mpz_class& pubKey=0
    ) = 0;
    virtual ~Cipher() = default;

protected:
    std::string readFile(const std::string& filePath);
    void printRunHeader(const std::string& cipherName,
                        const std::string& operation,
                        const std::string& filePath);
};

#endif