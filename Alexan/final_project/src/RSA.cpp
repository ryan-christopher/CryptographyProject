#include "RSA.h"
#include "Bootstrap.h"
#include "BBSRandom.h"
#include "crypto_utils.h"
#include "string_utils.h"
#include <fstream>
#include <iostream>
#include <sstream>

RSA::RSA(const std::string& publicKeyFile,
         const std::string& privateKeyFile,
         const mpz_class& minPrime,
         const mpz_class& maxPrime)
    : publicKeyFile(publicKeyFile), privateKeyFile(privateKeyFile)
{
    if (loadKeys()) {
        std::cerr << "Loaded existing RSA keys from:\n";
        std::cerr << "  Public:  " << publicKeyFile << std::endl;
        std::cerr << "  Private: " << privateKeyFile << std::endl;
    } else {
        std::cerr << "No existing RSA keys found. Generating new keys...\n";
        std::cerr << "  Prime range: [" << minPrime << ", " << maxPrime << "]\n";

        generateKeys(minPrime, maxPrime);
        saveKeys();

        std::cerr << "Keys generated and saved to:\n";
        std::cerr << "  Public:  " << publicKeyFile << std::endl;
        std::cerr << "  Private: " << privateKeyFile << std::endl;
    }
}

void RSA::generateKeys(const mpz_class& minPrime, const mpz_class& maxPrime)
{
    mpz_class p, q, phi_n;
    Bootstrap bootstrap;

    std::cerr << "Generating prime p...\n";
    p = bootstrap.generatePrimeInRange(minPrime, maxPrime);
    
    std::cerr << "Generating prime q...\n";
    q = bootstrap.generatePrimeInRange(minPrime, maxPrime);

    while (p == q) {
        q = bootstrap.generatePrimeInRange(minPrime, maxPrime);
    }

    n = p * q;
    phi_n = (p - 1) * (q - 1);
    e = 65537;  // a common choice

    while (!areRelativelyPrime(e, phi_n)) {
        e += 2;
    }

    d = modInverse(e, phi_n);

    mpz_class verify = (e * d) % phi_n;
    if (verify != 1) {
        throw std::runtime_error("Key generation failed: e*d mod φ(n) != 1");
    }
}

bool RSA::saveKeyFile(const std::string& filePath, const mpz_class& x) const
{
    std::ofstream outfile(filePath);
    if (!outfile.is_open()) return false;

    outfile << n << std::endl;
    outfile << x << std::endl;
    outfile.close();
    return true;
}

void RSA::saveKeys()
{
    // Save public key (n, e).
    if (!saveKeyFile(publicKeyFile, e)) {
        std::string msg = "Could not create public key file: " + publicKeyFile;
        throw std::runtime_error(msg);
    }

    // Save private key (n, d).
    if (!saveKeyFile(privateKeyFile, d)) {
        std::string msg = "Could not create private key file: " + privateKeyFile;
        throw std::runtime_error(msg);
    }
}

bool RSA::loadKeys()
{
    // Load public key.
    try {
        const std::pair<mpz_class, mpz_class> pubKey = readKeyFile(publicKeyFile);
        n = pubKey.first;
        e = pubKey.second;
    } catch (const std::runtime_error& err) {
        return false;
    }

    // Load private key.
    try {
        const std::pair<mpz_class, mpz_class> privKey = readKeyFile(privateKeyFile);
        d = privKey.second;
    } catch (const std::runtime_error& err) {
        return false;
    }

    return true;
}

mpz_class RSA::pollardsRho(const mpz_class& n)
{
    // Trivial cases
    if (n == 1) return n;
    if (n % 2 == 0) return 2;

    // Initialize with x = 5, y - 26 (as in lecture example)
    mpz_class x = 5;
    mpz_class y = 26;
    mpz_class d = 1;  // Our divisor of n.  It's either p or q.

    while (d == 1) {
        // f(x) = (x^2 + 1) % n
        x = (x * x + 1) % n;
        y = (y * y + 1) % n;
        y = (y * y + 1) % n;  // y takes 2 steps
        
        // Compute gcd(|x - y|, n)
        const mpz_class diff = (x > y) ? (x - y) : (y - x);
        d = findGCD(diff, n);

        // if d == n, then the algorithm failed (very rare)
        if (d == n) {
            // Restart with different initial values
            BBSRandom rng;
            x = rng.rand() % n;
            y = rng.rand() % n;
            d = 1;
        }
    }

    return d;
}

std::pair<mpz_class, mpz_class> RSA::readKeyFile(const std::string& filePath)
{
    std::ifstream keyFile(filePath);
    if (!keyFile.is_open()) {
        std::string ERR_MSG = "ERROR: Could not open key file: " + filePath;
        throw std::runtime_error(ERR_MSG);
    }

    std::string line;
    std::getline(keyFile, line);
    const mpz_class _n = mpz_class(line);
    std::getline(keyFile, line);
    const mpz_class e_or_d = mpz_class(line);
    keyFile.close();

    return std::make_pair(_n, e_or_d);
}

mpz_class RSA::attack(const std::string& cipherFilePath,
                      const std::string& targetPubKeyPath)
{
    std::cerr << "\n=== RSA (Factorization) ===\n\n";

    // Step 1: Read the target public key
    std::cerr << "Step 1: Read public key " << targetPubKeyPath  << "...\n\n";
    const std::pair<mpz_class, mpz_class> key = readKeyFile(targetPubKeyPath);
    const mpz_class _n = key.first;
    const mpz_class _e = key.second;

    // Step 2: Factor that n to get it's divisor, using Pollards Pho.
    //         The divisor could be p or q.  We don't know which one,
    //         but it doesn't matter.
    std::cerr << "Step 2: Finding divisor of n ...\n\n";
    const mpz_class p = pollardsRho(_n);
    const mpz_class q = _n / p;

    // Step 3: Calculate phi(n) = (p - 1)(q - 1)
    std::cerr << "Step 3: Calculating phi(" << _n << ") ...\n\n";
    const mpz_class phi = (p - 1) * (q - 1);

    // Step 4: Calculate private exponent d = e^(-1) % phi
    std::cerr << "Step 4: Calculating private exponent d ...\n\n";
    const mpz_class _d = modInverse(_e, phi);

    // Step 5: Read ciphertext
    std::cerr << "Step 5: Reading ciphertext from " << cipherFilePath << "...\n";
    mpz_class cipherText(readFile(cipherFilePath));

    // Step 6: Decrypt
    mpz_class plainText = modPow(cipherText, _d, _n);
    std::string msg = colorString(plainText.get_str());
    std::cerr << "\n✅ Successfully decrypted message: " << msg << std::endl;

    return plainText;
}

mpz_class RSA::decrypt(const mpz_class& cipherText)
{
    mpz_class clearText = modPow(cipherText, d, n);
    return clearText;
}

mpz_class RSA::encrypt(const mpz_class& clearText)
{
    mpz_class cipherText = modPow(clearText, e, n);
    return cipherText;
}

void RSA::run(const std::string& operation, const std::string& filePath, const mpz_class& pubKey)
{
    printRunHeader("RSA", operation, filePath);

    if (operation == "attack") {
        const std::string TARGET_PUBKEY = "./keys/target_rsa_key.pub";

        std::cout << attack(filePath, TARGET_PUBKEY) << std::endl;
        return;
    }
    
    const std::string textType = (operation == "decrypt") ? "cipher" : "clear";
    std::cerr << "Reading " << textType << "-text file: " << filePath << " ... ";
    const std::string text = readFile(filePath);
    std::cerr << "Done!\n";
    std::cerr << operation << "ing ... ";

    std::string output;

    if (operation == "encrypt") {
        mpz_class clear_n(text);
        output = encrypt(clear_n).get_str();
    } else {
        mpz_class cipher_n(text);
        output = decrypt(cipher_n).get_str();
    }

    std::cerr << "Done!\n";
    std::cout << output << std::endl;
}