#include "Cipher.h"
#include "string_utils.h"
#include <filesystem>
#include <fstream>
#include <iostream>
#include <sstream>
#include <stdexcept>

void Cipher::printRunHeader(const std::string& cipherName,
                               const std::string& operation,
                               const std::string& filePath)
{
    const bool attacking = operation == "attack";
    std::cerr << std::boolalpha
              << "Cipher:     " << cipherName << '\n'
              << "Operation:  " << colorString(operation, attacking) << '\n'
              << "Input File: " << filePath  << '\n';
}

std::string Cipher::readFile(const std::string& filePath)
{
    std::filesystem::path fp = filePath;
    if (!std::filesystem::exists(fp)) {
        throw std::runtime_error(
            "ERROR: File " + filePath + " does not exist."
        );
    }

    std::ifstream infile(filePath);
    if (!infile.is_open()) {
        throw std::runtime_error("ERROR: Could not open file: " + filePath);
    }

    std::stringstream buffer;
    buffer << infile.rdbuf();
    return buffer.str();
}