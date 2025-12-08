#!/bin/bash

pause() {
    echo ""
    read -n 1 -s -r -p "Press any key to continue to the next test..."
    echo ""
    echo ""
}

# El Gamal
echo "=== ElGamal Encrypt ==="
valgrind --leak-check=full ../bin/finalproject -a elgamal -o encrypt -i test_data/test_clear.txt > test_cipher_elgamal.txt
pause

echo "=== ElGamal Decrypt ==="
valgrind --leak-check=full ../bin/finalproject -a elgamal -o decrypt -i test_cipher_elgamal.txt
pause

echo "=== ElGamal Attack ==="
valgrind --leak-check=full ../bin/finalproject -a elgamal -o attack -i test_cipher_elgamal.txt
pause

# RSA
echo "=== RSA Encrypt ==="
valgrind --leak-check=full ../bin/finalproject -a rsa -o encrypt -i test_data/test_clear.txt > test_cipher_rsa.txt
pause

echo "=== RSA Decrypt ==="
valgrind --leak-check=full ../bin/finalproject -a rsa -o decrypt -i test_cipher_rsa.txt

echo ""
echo "=== All Valgrind tests complete ==="
