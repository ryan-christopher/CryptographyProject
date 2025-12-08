#!/bin/bash

YELLOW='\033[0;33m'
REDDISH_PINK='\033[35m'
NC='\033[0m' # No Color (resets the terminal color)

# Ryan
echo -e "${YELLOW}----------------------------------------------------------------${NC}"
echo -e "${YELLOW}| Encrypting a message TO Ryan, using his El Gamal public key. |${NC}"
echo -e "${YELLOW}----------------------------------------------------------------${NC}"
./bin/finalproject -a elgamal -o encrypt -i ./tests/test_data/test_clear.txt -p 720 -k ./keys/elgamal_key_ryan 
echo ""
echo -e "${YELLOW}------------------------------------------------------------------${NC}"
echo -e "${YELLOW}| Decrypting a message FROM Ryan, using my El Gamal private key. |${NC}"
echo -e "${YELLOW}------------------------------------------------------------------${NC}"
./bin/finalproject -a elgamal -o decrypt -i ./tests/test_data/ryans_cipher_elg.txt -k ./keys/elgamal_key
echo ""
echo -e "${YELLOW}------------------------------------------------------------------${NC}"
echo -e "${YELLOW}| Attacking an El Gamal encrypted message from Ryan to Leonidas. |${NC}"
echo -e "${YELLOW}------------------------------------------------------------------${NC}"
./bin/finalproject -a elgamal -o attack -i ./tests/test_data/ryans_cipher_elg2.txt -k ./keys/elgamal_key_leonidas 

echo -e "${YELLOW}----------------------------------------------------------------${NC}"
echo -e "${YELLOW}|    Encrypting a message TO Ryan, using his RSA public key.   |${NC}"
echo -e "${YELLOW}----------------------------------------------------------------${NC}"
./bin/finalproject -a rsa -o encrypt -i ./tests/test_data/test_clear.txt -p 5664221 -k ./keys/rsa_key_ryan
echo ""
echo -e "${YELLOW}-------------------------------------------------------------${NC}"
echo -e "${YELLOW}| Decrypting a message FROM Ryan, using my RSA private key. |${NC}"
echo -e "${YELLOW}-------------------------------------------------------------${NC}"
./bin/finalproject -a rsa -o decrypt -i ./tests/test_data/ryans_cipher_rsa.txt -k ./keys/rsa_key
echo ""
echo -e "${YELLOW}-------------------------------------------------------------${NC}"
echo -e "${YELLOW}| Attacking an RSA encrypted message from Ryan to Leonidas. |${NC}"
echo -e "${YELLOW}-------------------------------------------------------------${NC}"
cp ./keys/rsa_attack_ryan2leo.pub ./keys/target_rsa_key.pub
./bin/finalproject -a rsa -o attack -i ./tests/test_data/r2l_rsa_cipher.txt -k ./keys/target_rsa_key
# NOTE: Refer to the "Attacking RSA Ciphertext" section of README.md

# Leonidas
echo ""
echo -e "${REDDISH_PINK}--------------------------------------------------------------------${NC}"
echo -e "${REDDISH_PINK}| Encrypting a message TO Leonidas, using his El Gamal public key. |${NC}"
echo -e "${REDDISH_PINK}--------------------------------------------------------------------${NC}"
./bin/finalproject -a elgamal -o encrypt -i ./tests/test_data/test_clear_leonidas.txt -p 3124 -k ./keys/elgamal_key_leonidas

echo ""
echo -e "${REDDISH_PINK}----------------------------------------------------------------------${NC}"
echo -e "${REDDISH_PINK}| Decrypting a message FROM Leonidas, using my El Gamal private key. |${NC}"
echo -e "${REDDISH_PINK}----------------------------------------------------------------------${NC}"
./bin/finalproject -a elgamal -o decrypt -i ./tests/test_data/leonidas_cipher_elg.txt -k ./keys/elgamal_key

echo ""
echo -e "${REDDISH_PINK}------------------------------------------------------------------${NC}"
echo -e "${REDDISH_PINK}| Attacking an El Gamal encrypted message from Leonidas to Ryan. |${NC}"
echo -e "${REDDISH_PINK}------------------------------------------------------------------${NC}"
./bin/finalproject -a elgamal -o attack -i ./tests/test_data/leonidas_cipher_elg2.txt -k ./keys/elgamal_ryan2leonidas

echo ""
echo -e "${REDDISH_PINK}--------------------------------------------------------------------${NC}"
echo -e "${REDDISH_PINK}|    Encrypting a message TO Leonidas, using his RSA public key.   |${NC}"
echo -e "${REDDISH_PINK}--------------------------------------------------------------------${NC}"
./bin/finalproject -a rsa -o encrypt -i ./tests/test_data/test_clear.txt -p 65537 -k ./keys/rsa_key_leonidas

echo ""
echo -e "${REDDISH_PINK}-----------------------------------------------------------------${NC}"
echo -e "${REDDISH_PINK}| Decrypting a message FROM Leonidas, using my RSA private key. |${NC}"
echo -e "${REDDISH_PINK}-----------------------------------------------------------------${NC}"
./bin/finalproject -a rsa -o decrypt -i ./tests/test_data/leonidas_cipher_rsa.txt -k ./keys/rsa_key

echo ""
echo -e "${REDDISH_PINK}-------------------------------------------------------------${NC}"
echo -e "${REDDISH_PINK}| Attacking an RSA encrypted message from Leonidas to Ryan. |${NC}"
echo -e "${REDDISH_PINK}-------------------------------------------------------------${NC}"
cp ./keys/rsa_attack_leo2ryan.pub ./keys/target_rsa_key.pub
./bin/finalproject -a rsa -o attack -i ./tests/test_data/leonidas_cipher_rsa2.txt -k ./keys/rsa_leonidas2ryan
# NOTE: Refer to the "Attacking RSA Ciphertext" section of README.md
