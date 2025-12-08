# CS789 Final Project - Cryptography Implementation

Implementation of RSA and ElGamal encryption algorithms, with cryptanalysis attacks.

## Building
```bash
./build.sh
```

## Running

### For more details regarding CLI options
```bash
./bin/finalproject -?
```

### RSA
```bash
# Encrypt
./bin/finalproject -a rsa -o encrypt -p <Recipient Public Key> -i message.txt > cipher.txt

# Decrypt
./bin/finalproject -a rsa -o decrypt -i cipher.txt

# Attack (Pollards Rho)
./bin/finalproject -a rsa -o attack -i cipher.txt
```

### ElGamal
```bash
# Encrypt
./bin/finalproject -a elgamal -o encrypt -p <Recipient Public Key> -i message.txt > cipher.txt

# Decrypt
./bin/finalproject -a elgamal -o decrypt -i cipher.txt

# Attack (Baby-Step Giant-Step)
./bin/finalproject -a elgamal -o attack -i cipher.txt
```

### Custom Key Files
```bash
# Use custom key file names
./bin/finalproject -a rsa -o encrypt -i message.txt -k mykey
# Creates: mykey.pub and mykey
```

### Attacking RSA Ciphertext

To attack an RSA ciphertext without the private key, you need the public key that was used to encrypt it:
```bash
# 1. Obtain the victims public key and rename it
cp victim_rsa_key.pub target_rsa_key.pub

# 2. Run the attack (uses target_rsa_key.pub automatically)
./bin/finalproject -a rsa -o attack -i victim_cipher.txt
```

**Note:** The public key file must be named `target_rsa_key.pub` for RSA attacks.

### Complete Attack Demo
```bash
# Generate victims keys and encrypt a message
echo "42" > message.txt
./bin/finalproject -a rsa -o encrypt -i message.txt -k victim > victim_cipher.txt

# Prepare for attack: copy victims public key
cp victim.pub target_rsa_key.pub

# Generate your own keys (optional - to show they're separate)
./bin/finalproject -a rsa -o encrypt -i message.txt > /dev/null

# Attack the victims ciphertext
./bin/finalproject -a rsa -o attack -i victim_cipher.txt
# Output: 42
```

## Testing
```bash
cd tests
./test_elgamal.sh
./test_valgrind.sh
```

## Dependencies

- C++17 compiler
- [morrisfranken/argparse library](https://github.com/morrisfranken/argparse)
- [GMP library](https://gmplib.org/) (GNU Multiple Precision Arithmetic Library)
- [Valgrind](https://valgrind.org/) (**Optional**; Only needed for running `tests/test_valgrind.sh`)

## Algorithms Implemented

### RSA
- Key generation with random primes
- Encryption: c = m^e % n
- Decryption: m = c^d % n
- Attack: Pollards Rho factorization

### ElGamal
- Key generation with generator finding
- Encryption: (c1, c2) = (g^k mod p, m*y^k % p)
- Decryption: m = c2*(c1^x)^(-1) % p
- Attack: Baby-Step Giant-Step discrete logarithm