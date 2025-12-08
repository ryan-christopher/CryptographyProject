#include "ElGamal.h"
#include "Bootstrap.h"
#include "crypto_utils.h"
#include "string_utils.h"
#include <fstream>
#include <iostream>
#include <gmp.h>
#include <gmpxx.h>
#include <map>
#include <sstream>

ElGamal::ElGamal(const std::string& publicKeyFile,
                 const std::string& privateKeyFile,
                 const mpz_class& minRandomNumber,
                 const mpz_class& maxRandomNumber)
        : publicKeyFile(publicKeyFile), privateKeyFile(privateKeyFile)
{
    if (loadKeys()) {
        std::cerr << "Loaded existing El Gamal keys from:\n";
        std::cerr << "  Public:  " << publicKeyFile << std::endl;
        std::cerr << "  Private: " << privateKeyFile << std::endl;
    } else {
        std::cerr << "No existing El Gamal keys found. Generating new keys...\n";
        std::cerr << "  Prime range: [" << minRandomNumber << ", " << maxRandomNumber << "]\n";

        generateKeys(minRandomNumber, maxRandomNumber);
        saveKeys();

        std::cerr << "Keys generated and saved to:\n";
        std::cerr << "  Public:  " << publicKeyFile << std::endl;
        std::cerr << "  Private: " << privateKeyFile << std::endl;
    }
}

void ElGamal::generateKeys(const mpz_class& min, const mpz_class& max)
{
    Bootstrap bootstrap;
    p = bootstrap.generatePrimeInRange(min, max);
    g = findGenerator(p);
    privateKey = bootstrap.randomInRange(2, p - 2);
    publicKey = modPow(g, privateKey, p);
}

bool ElGamal::loadKeys()
{
    // Load public key.
    std::ifstream pubFile(publicKeyFile);
    if (!pubFile.is_open()) {
        return false;
    }

    std::string line;
    std::getline(pubFile, line);
    p = mpz_class(line);
    std::getline(pubFile, line);
    g = mpz_class(line);
    std::getline(pubFile, line);
    publicKey = mpz_class(line);
    pubFile.close();

    // Load private key.
    std::ifstream privFile(privateKeyFile);
    if (!privFile.is_open()) {
        return false;
    }

    std::getline(privFile, line);  // n is already loaded.
    privateKey = mpz_class(line);
    privFile.close();

    return true;
}

void ElGamal::saveKeys()
{
    std::ofstream pubFile(publicKeyFile);
    if (!pubFile.is_open()) {
        std::string msg = "Could not create public key file: " + publicKeyFile;
        throw std::runtime_error(msg);
    }

    pubFile << p << std::endl;
    pubFile << g << std::endl;
    pubFile << publicKey << std::endl;
    pubFile.close();

    std::ofstream privFile(privateKeyFile);
    if (!privFile.is_open()) {
        std::string msg = "Could not create private key file: " + privateKeyFile;
        throw std::runtime_error(msg);
    }

    privFile << privateKey << std::endl;
    privFile.close();
}

mpz_class ElGamal::babyStepGiantStep(const mpz_class& a,
                                     const mpz_class& g,
                                     const mpz_class& p)
{
    const std::string MSG_RUNNING = "Running Baby-Step Giant-Step attack...";
    std::cerr << colorString(MSG_RUNNING, true) << std::endl;
    std::cerr << "Solving: " << a << "^x ≡ " << g << " (mod " << p << ")\n";

    /*
        This function will solve for x in the congruency of
        a^x ≡ g % p
    */
    // Step 1: Compute m = ceil(sqrt(p))
    mpz_class m = sqrt(p);
    m += 1;  // Ceiling (since sqrt gives floor)
    // Since GMP library has no ceiling() function, this will have to do.
    // m is the number of steps we will need for our next 2 steps.

    std::cerr << "m = " << m << " (will need up to " << m << " steps)\n";

    // Step 2: Baby step - build table L1: a^(m*j) mod p for j = 0, 1, ..., m-1
    std::cerr << "Baby step: Computing a^(m*j) mod p...\n";
    std::map<mpz_class, mpz_class> L1;

    mpz_class a_m = modPow(a, m, p);
    mpz_class value = 1;

    for (mpz_class j = 0; j < m; j++) {
        L1[value] = j;
        value = (value * a_m) % p;
    }

    std::cerr << "Baby step complete. Table size: " << L1.size() << "\n";

    // Step 3: Giant step - compute g * a^(-i) mod p for i = 0, 1, ..., m-1
    std::cerr << "Giant step: Searching for collision...\n";

    mpz_class a_inv = modInverse(a, p);
    mpz_class gamma = g;

    for (mpz_class i = 0; i < m; i++) {
        // Check if gamma is in L1 table
        if (L1.count(gamma) > 0) {
            mpz_class j = L1[gamma];
            mpz_class x = m * j - i;
            
            std::cerr << "Match found! L2[" << i << "] = L1[" << j << "] = " << gamma << "\n";
            std::cerr << "i = " << i << ", j = " << j << "\n";
            std::cerr << "Private key x = " << x << "\n";
            
            // Verify the solution
            mpz_class check = modPow(a, x, p);
            if (check == g) {
                std::cerr << "✅ Verified: " << a << "^" << x << " ≡ " << g << " (mod " << p << ")\n";
                return x;
            } else {
                std::cerr << "⚠️ Verification failed with m*j - i, trying m*j + i...\n";
                x = m * j + i;  // Try alternate formula
                check = modPow(a, x, p);
                if (check == g) {
                    std::cerr << "✅ Verified: " << a << "^" << x << " ≡ " << g << " (mod " << p << ")\n";
                    return x;
                }
            }
        }
        
        gamma = (gamma * a_inv) % p;
    }
    
    throw std::runtime_error("Baby-Step Giant-Step failed to find x");
}

mpz_class ElGamal::attack(const std::string& cipherFilePath)
{
    std::cerr << "\n=== ElGamal Attack (Discrete Logarithm) ===\n";
    
    // Step 1: Use Baby-Step Giant-Step to recover private key x
    std::cerr << "\nStep 1: Recovering private key x from public key (p, g, publicKey)...\n";
    mpz_class recovered_x = babyStepGiantStep(g, publicKey, p);

    std::cerr << "\n✅ Successfully recovered private key: x = " << recovered_x << std::endl;

    // Step 2: Read ciphertext
    std::cerr << "\nStep 2: Reading ciphertext from " << cipherFilePath << "...\n";
    std::string text = readFile(cipherFilePath);

    std::istringstream iss(text);
    std::string line1, line2;
    std::getline(iss, line1);
    std::getline(iss, line2);

    mpz_class c1(line1);
    mpz_class c2(line2);

    std::cerr << "Ciphertext: (" << c1 << ", " << c2 << ")\n";
    
    // Step 3: Decrypt using recovered private key
    std::cerr << "\nStep 3: Decrypting using recovered private key...\n";
    
    // Temporarily save recovered key
    mpz_class original_x = privateKey;
    privateKey = recovered_x;
    
    mpz_class plaintext = decrypt(std::make_pair(c1, c2));
    
    privateKey = original_x;  // Restore original x

    std::string msg = colorString(plaintext.get_str());
    std::cerr << "\n✅ Successfully decrypted message: " << msg << std::endl;
        
    return plaintext;
}

mpz_class ElGamal::decrypt(const std::pair<mpz_class, mpz_class>& cipherText)
{
    mpz_class publicValue = cipherText.first;  // g^k mod p
    mpz_class _cipherText = cipherText.second; // cipher text
    mpz_class s = modPow(publicValue, privateKey, p);  // Shared secret s = publicValue^x mod p
    mpz_class s_inv = modInverse(s, p);  // Modular inverse of s, s^(-1) mod p
    mpz_class clearText = (_cipherText * s_inv) % p;
    return clearText;
}

std::pair<mpz_class, mpz_class> ElGamal::encrypt(const mpz_class& clearText, 
                                                 const mpz_class& pubKey)
{
    if (clearText <= 0 || clearText >= p) {
        const std::string ERR_MSG = "ERROR: Message must be in range [1, p-1]";
        throw std::invalid_argument(ERR_MSG);
    }

    Bootstrap bootstrap;
    mpz_class k = bootstrap.randomInRange(2, p - 2);  // used once, then destroyed
    mpz_class publicValue = modPow(g, k, p);  // g^k mod p
    mpz_class cipherText = (clearText * modPow(pubKey, k, p)) % p;

    return std::make_pair(publicValue, cipherText);
}

void ElGamal::run(const std::string& operation, const std::string& filePath, const mpz_class& pubKey)
{
    printRunHeader("El Gamal", operation, filePath);

    if (operation == "attack") {
        std::cout << attack(filePath) << std::endl;
        return;
    }

    const std::string textType = (operation == "decrypt") ? "cipher" : "clear";
    std::cerr << "Reading " << textType << "-text file: " << filePath << " ... ";
    const std::string text = readFile(filePath);
    std::cerr << "Done!\n";
    std::cerr << operation << "ing ... ";

    std::string output;

    if (operation == "encrypt") {
        mpz_class clearText(text);
        //mpz_class clearText(text, 10);
        std::cerr << "CLEAR TEXT:  " << clearText << '\n';
        std::pair<mpz_class, mpz_class> cipher = encrypt(clearText, pubKey);
        output = cipher.first.get_str() + "\n" + cipher.second.get_str();
        std::cerr << "My prime (p) is:     " << p << '\n';
        std::cerr << "My generator (g) is: " << g << '\n';
    } else {
        std::istringstream iss(text);
        std::string line1, line2;
        std::getline(iss, line1);
        std::getline(iss, line2);

        mpz_class c1(line1);
        mpz_class c2(line2);

        mpz_class clearText = decrypt(std::make_pair(c1, c2));
        output = clearText.get_str();
    }

    std::cerr << "Done!\n";
    std::cout << output << std::endl;
}